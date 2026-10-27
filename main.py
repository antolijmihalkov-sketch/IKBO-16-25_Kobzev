import tkinter as tk
import os
import argparse

class EmulatorApp:
    def __init__(self, root, vfs_path, prompt, script_path):
        self.root = root
        self.root.title(f"VFS: {os.path.basename(vfs_path)}")
        self.root.geometry("600x400")
        
        self.prompt = prompt
        self.script_path = script_path
        self.vfs_path = vfs_path
        
        if not os.path.exists(self.vfs_path) or not os.path.isdir(self.vfs_path):
            print(f"ОШИБКА: Папка VFS '{self.vfs_path}' не найдена! Создаю пустую...")
            os.makedirs(self.vfs_path, exist_ok=True)
            
        self.current_dir = self.vfs_path 
        self.history = [] # Для команды history

        self.output_text = tk.Text(root, height=15, width=70, state=tk.DISABLED)
        self.output_text.pack(pady=10, padx=10)

        input_frame = tk.Frame(root)
        input_frame.pack(fill=tk.X, padx=10)
        
        self.prompt_label = tk.Label(input_frame, text=self.prompt)
        self.prompt_label.pack(side=tk.LEFT)
        
        self.input_entry = tk.Entry(input_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.bind("<Return>", lambda event: self.execute_from_gui())

        self.run_button = tk.Button(root, text="Выполнить", command=self.execute_from_gui)
        self.run_button.pack(pady=5)

        if self.script_path:
            self.root.after(500, self.run_startup_script)

    def print_to_console(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

    def clear_console(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)

    def parse_input(self, text):
        args = []
        current_arg = ""
        in_quotes = False
        for char in text:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ' ' and not in_quotes:
                if current_arg:
                    args.append(current_arg)
                    current_arg = ""
            else:
                current_arg += char
        if current_arg:
            args.append(current_arg)
        return args

    def process_command(self, raw_input):
        # Не добавляем в историю пустые строки
        if not raw_input.strip():
            return True
            
        self.history.append(raw_input) # Сохраняем в историю
        self.print_to_console(f"{self.prompt}{raw_input}")
        args = self.parse_input(raw_input)
        if not args:
            return True
            
        command = args[0]
        command_args = args[1:]

        if command == "exit":
            self.root.quit()
            return True
        
        elif command == "help": # ЭТАП 5
            self.print_to_console("Доступные команды:")
            self.print_to_console("  ls           - список файлов и папок")
            self.print_to_console("  cd <путь>    - перейти в папку (cd .. - назад)")
            self.print_to_console("  head <файл>  - первые 10 строк файла")
            self.print_to_console("  history      - история команд")
            self.print_to_console("  clear        - очистить экран")
            self.print_to_console("  mkdir <имя>  - создать папку")
            self.print_to_console("  rmdir <имя>  - удалить пустую папку")
            self.print_to_console("  exit         - выход")

        elif command == "history": # ЭТАП 4
            for i, cmd in enumerate(self.history, 1):
                self.print_to_console(f"  {i}  {cmd}")

        elif command == "clear": # ЭТАП 4
            self.clear_console()

        elif command == "head": # ЭТАП 4
            if not command_args:
                self.print_to_console("Ошибка: укажите имя файла.")
                return False
            filename = command_args[0]
            path = os.path.join(self.current_dir, filename)
            if os.path.isfile(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        for _ in range(10):
                            line = f.readline()
                            if not line: break
                            self.print_to_console(line.rstrip())
                except Exception as e:
                    self.print_to_console(f"Ошибка чтения файла: {e}")
            else:
                self.print_to_console(f"Ошибка: файл '{filename}' не найден.")

        elif command == "mkdir": # ЭТАП 5
            if not command_args:
                self.print_to_console("Ошибка: укажите имя папки.")
                return False
            new_dir = os.path.join(self.current_dir, command_args[0])
            try:
                os.mkdir(new_dir)
                self.print_to_console(f"Папка '{command_args[0]}' создана.")
            except FileExistsError:
                self.print_to_console("Ошибка: папка уже существует.")
            except Exception as e:
                self.print_to_console(f"Ошибка: {e}")

        elif command == "rmdir": # ЭТАП 5
            if not command_args:
                self.print_to_console("Ошибка: укажите имя папки.")
                return False
            target_dir = os.path.join(self.current_dir, command_args[0])
            if os.path.isdir(target_dir):
                try:
                    os.rmdir(target_dir)
                    self.print_to_console(f"Папка '{command_args[0]}' удалена.")
                except OSError:
                    self.print_to_console("Ошибка: папка не пуста или нет прав.")
            else:
                self.print_to_console("Ошибка: папка не найдена.")

        elif command == "ls":
            try:
                files = os.listdir(self.current_dir)
                if not files:
                    self.print_to_console("(папка пуста)")
                else:
                    for f in files:
                        path = os.path.join(self.current_dir, f)
                        prefix = "d " if os.path.isdir(path) else "- "
                        self.print_to_console(f"{prefix}{f}")
            except Exception as e:
                self.print_to_console(f"Ошибка чтения папки: {e}")

        elif command == "cd":
            if not command_args:
                self.current_dir = self.vfs_path
                return True
            
            target = command_args[0]
            if target == "..":
                new_path = os.path.dirname(self.current_dir)
                if new_path.startswith(self.vfs_path):
                    self.current_dir = new_path
                else:
                    self.print_to_console("Ошибка: нельзя выйти за пределы VFS")
            else:
                new_path = os.path.join(self.current_dir, target)
                if os.path.isdir(new_path):
                    self.current_dir = new_path
                else:
                    self.print_to_console(f"Ошибка: папка '{target}' не найдена.")
        else:
            self.print_to_console(f"Ошибка: команда '{command}' не найдена.")
            return False
        return True

    def execute_from_gui(self):
        raw_input = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)
        if not raw_input:
            return
        self.process_command(raw_input)

    def run_startup_script(self):
        if not os.path.exists(self.script_path):
            self.print_to_console(f"Ошибка: Скрипт '{self.script_path}' не найден.")
            return

        self.print_to_console(f"--- Выполнение стартового скрипта: {self.script_path} ---")
        try:
            with open(self.script_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    success = self.process_command(line)
                    if not success:
                        self.print_to_console(f"(Строка пропущена из-за ошибки)")
        except Exception as e:
            self.print_to_console(f"Ошибка чтения скрипта: {e}")
        self.print_to_console("--- Скрипт завершен ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Эмулятор оболочки ОС")
    parser.add_argument("--vfs", required=True, help="Путь к папке VFS")
    parser.add_argument("--prompt", default="user@host:~$ ", help="Строка приглашения")
    parser.add_argument("--script", default=None, help="Путь к стартовому скрипту")
    
    args = parser.parse_args()

    print("=== ОТЛАДОЧНЫЙ ВЫВОД ПАРАМЕТРОВ ===")
    print(f"Путь к VFS: {args.vfs}")
    print(f"Приглашение: {args.prompt}")
    print(f"Стартовый скрипт: {args.script}")
    print("===================================")

    root = tk.Tk()
    app = EmulatorApp(root, args.vfs, args.prompt, args.script)
    root.mainloop()

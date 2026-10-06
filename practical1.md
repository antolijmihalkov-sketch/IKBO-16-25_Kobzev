# Практическое занятие №1

П.Н. Советов, РТУ МИРЭА

Научиться выполнять простые действия с файлами и каталогами в Linux из командной строки.

## Задача 1

Вывести отсортированный в алфавитном порядке список имён пользователей из `/etc/passwd`.

**Код (`task1.sh`):**

```bash
#!/bin/bash

grep -o '^[^:]*' /etc/passwd | sort
```

**Запуск:**

```bash
./task1.sh
```

**Результат:**

```text
_apt
backup
bin
daemon
games
...
```

## Задача 2

Топ-5 портов из `/etc/protocols`.

**Код (`task2.sh`):**

```bash
#!/bin/bash

grep -v '^#' /etc/protocols | awk 'NF {print $2, $1}' | sort -nr | head -n 5
```

**Запуск:**

```bash
./task2.sh
```

**Результат:**

```text
262 mptcp
143 ethernet
142 rohc
141 wesp
140 shim6
```

## Задача 3

Программа `banner` — вывод текста в рамке, размер меняется.

**Код (`banner`):**

```bash
#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <text>" >&2
    exit 1
fi

text="$1"
len=${#text}
border=$(printf '%*s' "$((len + 2))" '' | tr ' ' '-')

printf '+%s+\n' "$border"
printf '| %s |\n' "$text"
printf '+%s+\n' "$border"
```

**Запуск:**

```bash
./banner "Hello from RTU MIREA!"
```

**Результат:**

```text
+-----------------------+
| Hello from RTU MIREA! |
+-----------------------+
```

## Задача 4

Идентификаторы C/C++/Java в файле (без повторов).

**Код (`task4.sh`):**

```bash
#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file>" >&2
    exit 1
fi

grep -oE '[A-Za-z_][A-Za-z0-9_]*' "$1" | sort -u | tr '\n' ' '
echo
```

**Запуск:**

```bash
./task4.sh hello.c
```

**Результат:**

```text
Hello h include int main n printf return stdio void world
```

## Задача 5

Программа `reg` — регистрация команды в `/usr/local/bin`.

**Код (`reg`):**

```bash
#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <command>" >&2
    exit 1
fi

cmd="$1"

if [ ! -f "$cmd" ]; then
    echo "File not found: $cmd" >&2
    exit 1
fi

if [ "$(id -u)" -eq 0 ]; then
    install -m 755 "$cmd" /usr/local/bin/
else
    sudo install -m 755 "$cmd" /usr/local/bin/
fi
```

**Запуск:**

```bash
./reg banner
```

## Задача 6

Проверка наличия комментария в первой строке `.c`, `.js`, `.py`.

**Код (`task6.sh`):**

```bash
#!/bin/bash

path="${1:-.}"

find "$path" -type f \( -name '*.c' -o -name '*.js' -o -name '*.py' \) -print0 |
while IFS= read -r -d '' file; do
    first_line=$(head -n 1 -- "$file")

    case "$file" in
        *.py)
            if [[ "$first_line" =~ ^[[:space:]]*# ]]; then
                echo "$file: есть комментарий"
            else
                echo "$file: нет комментария"
            fi
            ;;
        *.c|*.js)
            if [[ "$first_line" =~ ^[[:space:]]*(//|/\*) ]]; then
                echo "$file: есть комментарий"
            else
                echo "$file: нет комментария"
            fi
            ;;
    esac
done
```

**Запуск:**

```bash
./task6.sh
```

**Результат:**

```text
./hello.c: нет комментария
./test.c: есть комментарий
./test2.py: нет комментария
```

## Задача 7

Поиск дубликатов по содержимому.

**Код (`task7.sh`):**

```bash
#!/bin/bash

path="${1:-.}"

find "$path" -type f -exec sha256sum {} + | sort | awk '
{
    hash=$1
    $1=""
    sub(/^ /, "")
    file=$0

    if (hash == prev_hash) {
        if (!printed) {
            print prev_file
            printed=1
        }
        print file
    } else {
        prev_hash=hash
        prev_file=file
        printed=0
    }
}'
```

**Запуск:**

```bash
./task7.sh testdir
```

**Результат:**

```text
testdir/a.txt
testdir/b.txt
```

## Задача 8

Архивация всех файлов с заданным расширением в tar.

**Код (`task8.sh`):**

```bash
#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <directory> <extension>" >&2
    exit 1
fi

dir="$1"
ext="$2"
archive="archive_${ext}.tar"

find "$dir" -type f -name "*.$ext" -print0 | tar --null -cvf "$archive" -T -
```

**Запуск:**

```bash
./task8.sh testdir txt
```

**Результат:**

```text
testdir/a.txt
testdir/b.txt
testdir/c.txt
```

## Задача 9

Замена 4 пробелов на табуляцию.

**Код (`task9.sh`):**

```bash
#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input> <output>" >&2
    exit 1
fi

tab=$'\t'
sed "s/    /$tab/g" "$1" > "$2"
```

**Запуск:**

```bash
./task9.sh input.txt output.txt
cat -A output.txt
```

**Результат:**

```text
hello^Iworld^Itest$
```

## Задача 10

Вывод имён пустых текстовых файлов в директории.

**Код (`task10.sh`):**

```bash
#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory>" >&2
    exit 1
fi

find "$1" -maxdepth 1 -type f -empty -printf '%f\n'
```

**Запуск:**

```bash
./task10.sh testdir
```

**Результат:**

```text
empty1.txt
empty2.txt
```

# Практическое занятие №1

П.Н. Советов, РТУ МИРЭА

Научиться выполнять простые действия с файлами и каталогами в Linux из командной строки. Сравнить работу в командной строке Windows и Linux.

## Задача 1

Вывести отсортированный в алфавитном порядке список имён пользователей в файле `/etc/passwd`.

```bash
./task1.sh
```

Результат:

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

```bash
./task2.sh
```

Результат:

```text
262 mptcp
143 ethernet
142 rohc
141 wesp
140 shim6
```

## Задача 3

Программа `banner` — вывод текста в рамке, размер меняется.

```bash
./banner "Hello from RTU MIREA!"
```

Результат:

```text
+-----------------------+
| Hello from RTU MIREA! |
+-----------------------+
```

## Задача 4

Идентификаторы в файле (без повторов).

```bash
./task4.sh hello.c
```

Результат:

```text
hello h include int main n printf return stdio void world
```

## Задача 5

Программа `reg` — регистрация команды в `/usr/local/bin`.

```bash
./reg banner
```

## Задача 6

Проверка наличия комментария в первой строке `.c`, `.js`, `.py`.

```bash
./task6.sh
```

Результат:

```text
./hello.c: нет комментария
./test.c: есть комментарий
./test2.py: нет комментария
```

## Задача 7

Поиск дубликатов по содержимому.

```bash
./task7.sh testdir
```

Результат:

```text
testdir/a.txt
testdir/b.txt
```

## Задача 8

Архивация всех файлов с заданным расширением в tar.

```bash
./task8.sh testdir txt
```

Результат:

```text
testdir/a.txt
testdir/b.txt
testdir/c.txt
```

## Задача 9

Замена 4 пробелов на табуляцию.

```bash
./task9.sh input.txt output.txt
cat -A output.txt
```

Результат:

```text
hello^Iworld^Itest$
```

## Задача 10

Вывод имён пустых текстовых файлов в директории.

```bash
./task10.sh testdir
```

Результат:

```text
empty1.txt
empty2.txt
```

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

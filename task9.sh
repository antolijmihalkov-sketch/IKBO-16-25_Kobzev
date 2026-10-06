#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input> <output>" >&2
    exit 1
fi

tab=$'\t'
sed "s/    /$tab/g" "$1" > "$2"

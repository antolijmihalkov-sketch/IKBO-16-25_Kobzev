#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <directory> <extension>" >&2
    exit 1
fi

dir="$1"
ext="$2"
archive="archive_${ext}.tar"

find "$dir" -type f -name "*.$ext" -print0 | tar --null -cvf "$archive" -T -

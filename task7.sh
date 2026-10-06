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

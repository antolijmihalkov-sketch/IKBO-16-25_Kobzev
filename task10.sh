#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory>" >&2
    exit 1
fi

find "$1" -maxdepth 1 -type f -empty -printf '%f\n'

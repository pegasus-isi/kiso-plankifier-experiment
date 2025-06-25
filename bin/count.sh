#!/bin/bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: $0 <input-file> <output-file>"
    exit 1
fi

cat $1 | cut -d' ' -f2 | sort | uniq -c > $2

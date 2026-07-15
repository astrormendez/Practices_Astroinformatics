#!/bin/bash

for file in *.csv
do
    outfile="${file%.csv}.lc"
    cut -d',' -f1,2,8,9 "$file" | tr ',' ' ' > "$outfile"
done
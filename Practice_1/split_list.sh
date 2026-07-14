#!/bin/bash

split -l 5 -d csv_files.txt file_list_

for f in file_list_*; do
	mv "$f" "$f.txt"
done

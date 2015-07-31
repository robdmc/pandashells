#! /usr/bin/env bash

#p.crypt
echo 'plain text' > file.txt && p.crypt -i file.txt -v -o file.txt.crypt
p.crypt -d -i file.txt.crypt -o file_restored.txt 
echo Original
cat file.txt
echo
echo Final
cat file_restored.txt
rm file*


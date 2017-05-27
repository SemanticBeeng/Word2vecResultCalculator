#!/bin/bash
input="$1"

#echo $input
python create.py
./distance $input

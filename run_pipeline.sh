#!/bin/bash

# Get command line arguments
input_path="$1"
output_path="$2"

echo "Starting meta data checking..."
python nai_meta.py $input_path

echo "Starting sorting..."
python nai_sort.py $output_path
echo "Pipeline completed."
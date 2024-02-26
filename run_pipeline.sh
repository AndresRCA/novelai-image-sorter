#!/bin/bash

echo "Starting meta data checking..."
python3 nai_meta.py

echo "Starting sorting..."
python3 nai_sort.py

echo "Pipeline completed."
#!/bin/bash

echo "Starting meta data checking..."
python nai_meta.py

echo "Starting sorting..."
python nai_sort.py

echo "Pipeline completed."
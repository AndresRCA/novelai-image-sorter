# NovelAI Image Metadata Scripts

These scripts extract metadata from images generated with NovelAI's image generation functionality and sort them based on their tag values.

## Contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [How to Use](#how-to-use)
4. [Sorting Process](#sorting-process)
5. [Advice for Effective Sorting](#advice-for-effective-sorting)
6. [Compatibility](#compatibility)

## Introduction
This repository contains two Python scripts, `nai_meta.py` and `nai_sort.py`, designed for handling image metadata and sorting images, respectively.

### `nai_meta.py`
This script extracts prompt information and other settings from the alpha channel of NAI generated images located in the `input/` folder. The extracted data is stored in a JSON file named `all_metadata.json`.

### `nai_sort.py`
The sorting script copies images from the `input/` folder and categorizes them into different folders within the `output/` directory based on their characteristics.

## Requirements
- Python 3
- NumPy package

## How to Use
**Command Usage**:
- `python nai_meta.py [input_path="./input"]`
- `python nai_sort.py [output_path="./output"]`


## Sorting Process
To sort your images:

1. Ensure your Python environment is set up. Install the NumPy package using `pip install numpy`.
2. Place the images you wish to sort into the `input/` folder.
3. Run `nai_meta.py` to generate the `all_metadata.json` file containing metadata for all images.
4. Edit the `tags.py.example` file to specify the tags for sorting. Remove the `.example` suffix and populate the arrays with your desired tags.
5. Run `nai_sort.py` to sort the images into the `output/` folder.

### Advice for Effective Sorting
- Populate the character tag array with as many character cases as possible to avoid mixed character folders.
- Use complete tag names to ensure effective sorting.
- Regular tags should be unique and unrelated to each other for optimal sorting.
- Character tags and regular tags are treated as separate batches.
- Ensure the `input/` folder contains only image files supported by the script.

## Compatibility
The scripts work with images generated using NovelAI's image generation functionality. If images have not been altered, the scripts should successfully extract metadata from them. Otherwise, failed attempts are stored in the `output/failed attempts/` folder.
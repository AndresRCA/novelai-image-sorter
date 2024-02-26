import os
import shutil
import json
from tags import CHARACTER_TAGS, TAGS

def clear_output_directory(output_directory):
    if os.path.exists(output_directory):
        for item in os.listdir(output_directory):
            item_path = os.path.join(output_directory, item)
            if os.path.isfile(item_path) and item == ".gitkeep":
                continue
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)

def categorize_image(image_metadata, output_directory):
    description = image_metadata.get("Description", "").lower()
    file_name = image_metadata.get("File name")
    
    # Check for character tags
    char_tag_count = sum(description.count(tag.lower()) for tag in CHARACTER_TAGS)
    if char_tag_count == 1:
        for char_tag in CHARACTER_TAGS:
            if char_tag.lower() in description:
                char_tag_folder = os.path.join(output_directory, "character", char_tag)
                os.makedirs(char_tag_folder, exist_ok=True)
                shutil.copy(os.path.join("input", file_name), char_tag_folder)
                return True
    
    # Check for regular tags
    reg_tag_count = sum(description.count(tag.lower()) for tag in TAGS)
    if reg_tag_count == 1:
        for reg_tag in TAGS:
            if reg_tag.lower() in description:
                reg_tag_folder = os.path.join(output_directory, "tags", reg_tag)
                os.makedirs(reg_tag_folder, exist_ok=True)
                shutil.copy(os.path.join("input", file_name), reg_tag_folder)
                return True
    
    # If no or multiple tags match, move to unsorted folder
    unsorted_folder = os.path.join(output_directory, "unsorted")
    os.makedirs(unsorted_folder, exist_ok=True)
    shutil.copy(os.path.join("input", file_name), unsorted_folder)
    return False

def sort_images(metadata_file, output_directory):
    with open(metadata_file, 'r') as f:
        all_metadata = json.load(f)
    
    character_sorted = 0
    regular_sorted = 0
    unsorted = 0
    total_images = len(all_metadata)
    
    for i, metadata in enumerate(all_metadata, 1):
        print(f"Processing image {i}/{total_images}...")
        if categorize_image(metadata, output_directory):
            if i <= total_images // 2:  # First half for character tags, second half for regular tags
                character_sorted += 1
            else:
                regular_sorted += 1
        else:
            unsorted += 1
    
    print("Sorting completed.")
    print(f"Character tags sorted: {character_sorted}/{total_images}")
    print(f"Regular tags sorted: {regular_sorted}/{total_images}")
    print(f"Unsorted: {unsorted}/{total_images}")

# Define the paths
metadata_file = "all_metadata.json"
output_directory = "output"

# Clear the output directory
clear_output_directory(output_directory)

# Perform the sorting
sort_images(metadata_file, output_directory)

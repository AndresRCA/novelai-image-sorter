import os
import shutil
import json
import re
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
    file_path = image_metadata.get("File path")
    
    # Check for character tags
    characters_in_image = [tag for tag in CHARACTER_TAGS if re.search(r'(?<![^\W_]){0}(?![^\W_])'.format(re.escape(tag.lower())), description)]
    char_tag_count = len(characters_in_image)
    if char_tag_count == 1:
        char_tag = characters_in_image[0]
        char_tag_folder = os.path.join(output_directory, "character", char_tag)
        os.makedirs(char_tag_folder, exist_ok=True)
        shutil.copy(file_path, char_tag_folder)
        return True
    
    # Check for regular tags
    tags_in_image = [tag for tag in TAGS if re.search(r'(?<![^\W_]){0}(?![^\W_])'.format(re.escape(tag.lower())), description)]
    reg_tag_count = len(tags_in_image)
    if reg_tag_count == 1:
        reg_tag = tags_in_image[0]
        reg_tag_folder = os.path.join(output_directory, "tags", reg_tag)
        os.makedirs(reg_tag_folder, exist_ok=True)
        shutil.copy(file_path, reg_tag_folder)
        return True
    
    # If no or multiple tags match, move to unsorted folder
    unsorted_folder = os.path.join(output_directory, "unsorted")
    os.makedirs(unsorted_folder, exist_ok=True)
    shutil.copy(file_path, unsorted_folder)
    return False

def sort_images(metadata_file, output_directory):
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
        all_metadata = metadata.get("metadata", [])
    
    character_sorted = 0
    regular_sorted = 0
    unsorted = 0
    total_images = len(all_metadata)
    
    for i, image_metadata in enumerate(all_metadata, 1):
        print(f"Processing image {i}/{total_images}...")
        if categorize_image(image_metadata, output_directory):
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

def copy_failed_attempts_to_folder(output_directory, failed_files):
    unsorted_folder = os.path.join(output_directory, "failed attempts")
    os.makedirs(unsorted_folder, exist_ok=True)
    for failed_file in failed_files:
        source_path = failed_file  # Use full file path
        destination_path = os.path.join(unsorted_folder, os.path.basename(failed_file))  # Use only file name in destination
        shutil.copy2(source_path, destination_path)

# Define the paths
metadata_file = "all_metadata.json"
output_directory = "output"

# Clear the output directory
clear_output_directory(output_directory)

# Perform the sorting
sort_images(metadata_file, output_directory)

# Copy failed attempts to unsorted folder
with open(metadata_file, 'r') as f:
    metadata = json.load(f)
    failed_files = metadata.get("failed_files", [])
    copy_failed_attempts_to_folder(output_directory, failed_files)

print(f"{len(failed_files)} files that failed the meta data check were copied to the \"failed attempts\" folder.")

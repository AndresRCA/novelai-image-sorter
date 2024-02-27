import os
import argparse
from PIL import Image
import numpy as np
import gzip
import json

class LSBExtractor:
    def __init__(self, data):
        self.data = data
        self.rows, self.cols, self.dim = data.shape
        self.bits = 0
        self.byte = 0
        self.row = 0
        self.col = 0

    def _extract_next_bit(self):
        if self.row < self.rows and self.col < self.cols:
            bit = self.data[self.row, self.col, self.dim - 1] & 1
            self.bits += 1
            self.byte <<= 1
            self.byte |= bit
            self.row += 1
            if self.row == self.rows:
                self.row = 0
                self.col += 1
        else:
            self.bits = 8

    def get_one_byte(self):
        while self.bits < 8:
            self._extract_next_bit()
        byte = bytearray([self.byte])
        self.bits = 0
        self.byte = 0
        return byte

    def get_next_n_bytes(self, n):
        bytes_list = bytearray()
        for _ in range(n):
            byte = self.get_one_byte()
            if not byte:
                break
            bytes_list.extend(byte)
        return bytes_list

    def read_32bit_integer(self):
        bytes_list = self.get_next_n_bytes(4)
        if len(bytes_list) == 4:
            integer_value = int.from_bytes(bytes_list, byteorder='big')
            return integer_value
        else:
            return None

def process_images(directory):
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']
    all_metadata = []
    failed_files = []

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                file_path = os.path.join(root, filename)
                print(f"Processing {file_path}...")
                try:
                    img = Image.open(file_path)
                    img = np.array(img)
                    assert img.shape[-1] == 4 and len(img.shape) == 3, "image format"
                    reader = LSBExtractor(img)
                    magic = "stealth_pngcomp"
                    read_magic = reader.get_next_n_bytes(len(magic)).decode("utf-8")
                    assert magic == read_magic, "magic number"
                    read_len = reader.read_32bit_integer() // 8
                    json_data = reader.get_next_n_bytes(read_len)
                    json_data = json.loads(gzip.decompress(json_data).decode("utf-8"))
                    if "Comment" in json_data:
                        json_data["Comment"] = json.loads(json_data["Comment"])
                    json_data["File path"] = file_path  # Add the "File path" field
                    all_metadata.append(json_data)
                except Exception as e:
                    print(f"Failed to process {file_path}: {e}")
                    failed_files.append(file_path)

    # Write all metadata to a JSON file
    json_output_file = 'all_metadata.json'
    with open(json_output_file, 'w') as json_file:
        json.dump({"metadata": all_metadata, "failed_files": failed_files}, json_file, indent=4)

    print(f"All metadata saved to {json_output_file}.")

def main():
    default_input_path = os.path.join(os.getcwd(), "input")
    parser = argparse.ArgumentParser(description="Process images and extract metadata.")
    parser.add_argument("input_path", nargs="?", type=str, default=default_input_path, help="Path to the input folder containing images.")
    args = parser.parse_args()

    input_path = args.input_path
    process_images(input_path)

if __name__ == "__main__":
    main()

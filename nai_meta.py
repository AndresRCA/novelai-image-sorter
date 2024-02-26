import os
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

directory = 'input'  # directory with files

image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']

all_metadata = []

for filename in os.listdir(directory):
    if any(filename.lower().endswith(ext) for ext in image_extensions):
        file_path = os.path.join(directory, filename)
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
            json_data["File name"] = filename  # Add the "File name" field
            all_metadata.append(json_data)
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

# Write all metadata to a JSON file
json_output_file = 'all_metadata.json'
with open(json_output_file, 'w') as json_file:
    json.dump(all_metadata, json_file, indent=4)

print(f"All metadata saved to {json_output_file}.")

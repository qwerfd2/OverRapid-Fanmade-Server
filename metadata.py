import os
import hashlib
import json

def calculate_md5_and_size(file_path):
    md5_hash = hashlib.md5()
    file_size = 0

    with open(file_path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            md5_hash.update(byte_block)
            file_size += len(byte_block)

    return md5_hash.hexdigest(), file_size

def process_folder(folder_path):
    md5_checksum_dict = {}
    size_dict = {}

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, folder_path)
            
            md5_checksum, file_size = calculate_md5_and_size(file_path)
            
            md5_checksum_dict[relative_path.replace("\\", "/")] = md5_checksum
            size_dict[relative_path.replace("\\", "/")] = file_size

    return md5_checksum_dict, size_dict

def write_to_file(file_name, data):
    with open(file_name, "w") as file:
        file.write(json.dumps(data, separators=(',', ':')))

if __name__ == "__main__":
    resources_folder = "Resources"
    
    md5_checksum_dict, size_dict = process_folder(resources_folder)
    
    md5_file_name = "OverRide/Md5ListChecksum.json"
    size_file_name = "OverRide/SizeList.json"
    
    write_to_file(md5_file_name, md5_checksum_dict)
    write_to_file(size_file_name, size_dict)

    print(f"MD5 checksums saved to {md5_file_name}")
    print(f"File sizes saved to {size_file_name}")

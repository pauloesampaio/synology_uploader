import os
import zipfile
import io
import shutil

def compress_folder_to_memory(folder_path):
    # Create a BytesIO object to hold the in-memory ZIP file
    memory_file = io.BytesIO()
    
    # Create a ZipFile object with the BytesIO object
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the folder
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # Create the full file path
                file_path = os.path.join(root, file)
                # Add file to the zip archive
                zipf.write(file_path, os.path.relpath(file_path, folder_path))
    
    # Seek to the beginning of the BytesIO object
    memory_file.seek(0)
    
    return memory_file

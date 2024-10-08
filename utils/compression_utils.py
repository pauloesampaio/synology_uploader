import os
import zipfile
import io
import shutil

def compress_folder_to_memory(folder_path):
    # Create a BytesIO object to hold the in-memory ZIP file
    memory_file = io.BytesIO()
    
    # Extract the folder name from the folder path
    folder_name = os.path.basename(os.path.normpath(folder_path))
    
    # Create a ZipFile object with the BytesIO object
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the folder
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # Create the full file path
                file_path = os.path.join(root, file)
                # Create the archive name with the folder name prepended
                archive_name = os.path.join(folder_name, os.path.relpath(file_path, folder_path))
                # Add file to the zip archive
                zipf.write(file_path, archive_name)
    
    # Seek to the beginning of the BytesIO object
    memory_file.seek(0)
    
    return memory_file
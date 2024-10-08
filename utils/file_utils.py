import os

def list_available_folders(base_path, string_filter=None, string_remove_filter=None):
    all_items = os.listdir(base_path)
    only_folders = [item for item in all_items if os.path.isdir(os.path.join(base_path, item))]
    if string_filter:
        only_folders = [folder for folder in only_folders if string_filter in folder]
    if string_remove_filter:
        only_folders = [folder for folder in only_folders if string_remove_filter not in folder]
    return only_folders
import os
import shutil

def recursive_copy(src_dir: str, dst_dir: str):
    """
    Recursively copy files from source to destination directory while preserving structure.
    
    Args:
        src_dir: Source directory path
        dst_dir: Destination directory path

    Example:
        recursive_copy("path/to/source", "path/to/destination")
    """
    os.makedirs(dst_dir, exist_ok=True)
    
    for root, dirs, files in os.walk(src_dir):
        # Create directories
        for dir_name in dirs:
            src_path = os.path.join(root, dir_name)
            dst_path = os.path.join(dst_dir, os.path.relpath(src_path, src_dir))
            os.makedirs(dst_path, exist_ok=True)
        
        # Copy files
        for file_name in files:
            src_path = os.path.join(root, file_name)
            dst_path = os.path.join(dst_dir, os.path.relpath(src_path, src_dir))
            shutil.copy2(src_path, dst_path)
import os
import time
from tqdm import tqdm


def get_file_size(file_path):
    """
    Returns the size of a file in bytes
    """
    return os.path.getsize(file_path)


def is_old_file(file_path):
    """
    Checks if a file was accessed more than 2 hours ago
    """
    two_hours_ago = time.time() - 1000
    last_access_time = os.path.getatime(file_path)
    return last_access_time < two_hours_ago


def main():
    total_size = 0
    file_count = 0
    for root, dirs, files in os.walk(".", topdown=False):
        for file_name in tqdm(files, desc="Scanning files..."):
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                if get_file_size(file_path) > 104 and is_old_file(file_path):
                    file_count += 1
                    total_size += get_file_size(file_path)
                    print(f"{file_path}: {get_file_size(file_path) / 1048576:.2f} MB")
    print(f"\nFound {file_count} files > 1MB and not accessed in the last 2 hours.")
    print(f"Total size: {total_size / 1048576:.2f} MB")

    #print total size of the folder
    print("Total size of the folder: ", end="")



if __name__ == "__main__":
    main()

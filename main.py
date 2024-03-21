import tkinter as tk
from tkinter import filedialog
from PIL import Image
import numpy as np
import os
import shutil  # To copy files
import imageio.v2 as imageio  # Use imageio version 2 explicitly

def select_directory(title='Select Folder'):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    dir_path = filedialog.askdirectory(title=title)
    return dir_path

def select_files():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_paths = filedialog.askopenfilenames(title='Select DDS Files', filetypes=[("DDS files", "*.dds")])
    return root.tk.splitlist(file_paths)

def copy_file(src_path, dest_path):
    """
    Copies a file from src_path to dest_path.
    """
    shutil.copy2(src_path, dest_path)

def process_dds_file(file_path, dest_dir, copy_skipped_files, division_factor):
    try:
        img = imageio.imread(file_path)
        original_height, original_width = img.shape[:2]

        print(f"Processing {os.path.basename(file_path)}: original dimensions are {original_width}x{original_height}")

        # Check if image is larger than 128x128 and if dimensions are divisible by the division factor
        if original_width > 128 and original_height > 128 and original_width % division_factor == 0 and original_height % division_factor == 0:
            width, height = original_width // division_factor, original_height // division_factor
            img_resized = Image.fromarray(img).resize((width, height), Image.Resampling.LANCZOS)
            dest_path = os.path.join(dest_dir, os.path.basename(file_path))
            img_resized.save(dest_path)
            print(f"Saved processed file to {dest_path}, new dimensions: {width}x{height}")
        else:
            print(f"Skipping resizing for {file_path}.")
            if copy_skipped_files:
                dest_path = os.path.join(dest_dir, os.path.basename(file_path))
                copy_file(file_path, dest_path)
                print(f"Copied original file to {dest_path} without resizing.")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def process_files(files, dest_dir, copy_skipped_files, division_factor):
    for file_path in files:
        process_dds_file(file_path, dest_dir, copy_skipped_files, division_factor)

def main():
    choice = input("Type 'd' to select directory or 'f' to select files: ").lower()
    copy_choice = input("Copy files skipped for resizing to the destination directory? (y/n): ").lower()
    copy_skipped_files = copy_choice == 'y'
    division_factor = int(input("Enter the division factor for resizing (e.g., 2, 4): "))

    if choice == 'd':
        source_directory = select_directory('Select Source Folder with DDS Files')
        if source_directory:
            files = [os.path.join(source_directory, f) for f in os.listdir(source_directory) if f.endswith('.dds')]
            destination_directory = select_directory('Select Destination Folder for Processed Files')
            if destination_directory:
                process_files(files, destination_directory, copy_skipped_files, division_factor)
    elif choice == 'f':
        files = select_files()
        if files:
            destination_directory = select_directory('Select Destination Folder for Processed Files')
            if destination_directory:
                process_files(files, destination_directory, copy_skipped_files, division_factor)


if __name__ == "__main__":
    main()
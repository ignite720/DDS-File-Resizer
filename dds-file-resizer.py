from pathlib import Path

import tkinter as tk
from tkinter import filedialog
from PIL import Image
import numpy as np
import os
import imageio.v2 as imageio  # Use imageio version 2 explicitly

def select_directory(title='Select Folder'):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    dir_path = filedialog.askdirectory(title=title)
    return dir_path

def is_power_of_two(n):
    return (n != 0) and (n & (n - 1)) == 0

def get_image_resolution_slow(image_path):
    img = imageio.imread(image_path)
    original_height, original_width = img.shape[:2]
    return original_height, original_width
    
def get_image_resolution_fast(image_path):
    width, height = 0, 0
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height
    
def process_dds_file(file_path, threshold_width):
    try:
        original_height, original_width = get_image_resolution_fast(file_path)
        original_aspect_ratio = (original_width / original_height)
        print(f"Processing {os.path.basename(file_path)}: original dimensions are {original_width}x{original_height}, aspect ratio: {original_aspect_ratio}")
        
        if original_width > threshold_width and is_power_of_two(original_width) and is_power_of_two(original_height):
            new_width, new_height = int(threshold_width), int(threshold_width / original_aspect_ratio)
            
            img = imageio.imread(file_path)
            img_resized = Image.fromarray(img).resize((new_width, new_height), Image.Resampling.LANCZOS)
            img_resized.save(file_path)
            print(f"    > Saved processed file to {file_path}, new dimensions: {new_width}x{new_height}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_files(files, threshold_width):
    for file_path in files:
        process_dds_file(file_path, threshold_width)

def main():
    threshold_width = int(input("Enter the threshold_width for resizing (e.g., 512): "))
    #source_directory = select_directory('Select Source Folder with DDS Files')
    source_directory = Path.cwd()
    if source_directory:
        files = [os.path.join(root, f) for root, dirs, filenames in os.walk(source_directory) for f in filenames if f.endswith('.dds')]
        process_files(files, threshold_width)

if __name__ == "__main__":
    main()
import os
import shutil

# Create the new directory
new_dir = "Jan 2025"
if not os.path.exists(new_dir):
    os.makedirs(new_dir)

# List of PNG files to move
png_files = [
    "rp1_progress.png",
    "abidjan_progress.png",
    "johannesburg_progress.png",
    "overall_progress.png"
]

# Move each PNG file to the new directory
for file in png_files:
    if os.path.exists(file):
        shutil.move(file, os.path.join(new_dir, file))
        print(f"Moved {file} to {new_dir}/")
    else:
        print(f"File {file} not found")

#!/usr/bin/env python3

'''

A script to modify the images in the images directory is needed to stage images to be uploaded to a website.  The images need to have specific
dimensions, orientation and be in jpeg format. They change often and there will be large batches of images to be modified regularly.

'''

# Import the Image method from PIL
from PIL import Image
# Import Path from pathLib to handle file paths
from pathlib import Path
# Import os to call 'open' on the dice.jpeg file
import subprocess


# Set relative path to the image directory
image_dir = Path(__file__).parent.parent / 'data' / 'images'
image_dir_modified = Path(__file__).parent.parent / 'data' / 'images_modified'

# Get a list of files that are in "image_dir"
ls_files = [files.name for files in image_dir.iterdir()]
print(ls_files)

# Iterating over the list of files obtained
for file in ls_files:
    if "." not in file[0]:
      file_img = Image.open(image_dir / file)   # For each image file create an Image instance
      file_img.rotate(90).save(image_dir_modified / f"{file}_90.jpeg")
      file_img.resize((128,128)).save(image_dir_modified / f"{file}._128x128.jpeg")
      file_img.rotate(-90).resize((128,128)).save(image_dir_modified / f"{file}.flipped_rotated.jpeg")
      subprocess.run(["open", str(image_dir_modified / f"{file}_90.jpeg")])
      subprocess.run(["open", str(image_dir_modified / f"{file}._128x128.jpeg")])


""" RUNTIME:

/usr/local/bin/python3.14 /Users/admin/PycharmProjects/PythonProject/Coursera_GoogleITAutomation_Projects/Projects_6/Scale-Convert-Images/scripts/modify_images.py 
['.DS_Store', 'at3_1m4_01(1).tif', 'dice.jpg', 'bischon.jpg', 'autumn.tif']

Process finished with exit code 0


"""
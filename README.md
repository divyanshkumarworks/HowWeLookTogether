# HowWeLookTogether
# About

Developed a web app for matrimonial use-case where picture of two persons can be uploaded to see how they will look if stood next to each other The app takes images of two person with their height as input and outputs
a final image which contains cutouts of both person placed side by side on a separate background image. The app first crops out persons from their respective original images,
resizes them according to the persons height and merges them side by side on a default background image

## Features

- Drag and drop images 
- preview and save images
- Support JPG, PNG file fromats
- Image optimization, automatic image resizing, cropping, and fixes EXIF orientation.

## Installation
1. Clone this repository
2. Install dependencies
   
   ```bash
   pip3 install -r requirements.txt
   ```
4. Download the pre-trained weights and place it inside the root directory. The weights can be downloaded from this link: https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5.

3. Run the website from the root directory
    ```bash
    python manage.py runserver
    ```


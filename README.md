# HowWeLookTogether
# About

Developed a web app for matrimonial use-case where picture of two persons can be uploaded to see how they will look if stood next to each other The app takes images of two person with their height as input and outputs
a final image which contains cutouts of both person placed side by side on a separate background image. The app first crops out persons from their respective original images,
resizes them according to the persons height and merges them side by side on a default background image

## Features

- Drag and drop images 
- preview and save images
- Support JPG, PNG file fromats

## Installation
1. Clone this repository
2. Install dependencies
   
   ```bash
   pip3 install -r requirements.txt
   ```
3. Run the website from the root directory
    ```bash
    python manage.py runserver
    ``` 

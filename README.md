# HowWeLookTogether
# About

Developed a web app for matrimonial use-case where picture of two persons can be uploaded to see how they will look if stood next to each other. The app takes images of two person with their height as input and outputs
a final image which contains cutouts of both person placed side by side on a separate background image. The app first crops out persons from their respective original images,
resizes them according to the persons height and merges them side by side on a default background image

## Screenshots

📌 Landing Page

![Screenshot (47)](https://github.com/divyanshkumarworks/heavy-reminder/assets/134360630/e96a2de7-0a11-4d3c-8661-743731475464)

📌 Home Page

![Screenshot (49)](https://github.com/divyanshkumarworks/heavy-reminder/assets/134360630/2dfbba11-c114-4f19-af57-c03388c50040)

📌 Waiting Page

![Screenshot (50)](https://github.com/divyanshkumarworks/heavy-reminder/assets/134360630/0bf2ea8f-c6fe-4d39-84bb-13fd984fc7f8)

## Overview

This project implements Mask_RCNN_TF2 based on tensorflow 2.0, keras 2.2.4 and above. This project uses Mask_RCNN for extracting person mask and bounding boxes for cropping and creating png image. Resizes person's height with respect to another person's height and pastes both the images side by side using [Open_CV](https://www.geeksforgeeks.org/opencv-overview/) and overlays the image on a deafult background with the help of cvzone library. 

#### What is Mask_RCNN?
Mask RCNN is a deep neural network aimed to solve instance segmentation problem in machine learning or computer vision. The model generates bounding boxes and segmentation masks for each instance of an object in the image. It's based on Feature Pyramid Network (FPN) and a ResNet101 backbone. Learn more about Mask_RCNN on this page: https://github.com/ahmedfgad/Mask-RCNN-TF2

## Features

- Drag and drop images 
- preview and save images
- Support JPG, PNG file fromats
- Image optimization, automatic image resizing, cropping, and fixes EXIF orientation.

## Installation
1. Clone this repository
   ```bash
   https://github.com/divyanshkumarworks/Blogging-Portal.git
   ```
2. Create Virtual Environment
   ```bash
   python3 -m venv venv
   ```
3. Activate the environment
   ```bash
   source /venv/bin/activate
   ```

4. Install dependencies
   ```bash
   pip3 install -r requirements.txt
   ```
5. The pre-trained weights of the Mask R-CNN model is based on the COCO dataset. The weights can be downloaded from this link: https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5. After downloading the weights, place it inside the root directory.

   The COCO dataset has 80 classes. There is an additional class for the background named **BG**. Thus, the total number of classes is 81. The classes names are listed in the `CLASS_NAMES` list. **DO NOT CHANGE THE ORDER OF THE CLASSES**.

6. Run the website from the root directory
    ```bash
    python manage.py runserver
    ```


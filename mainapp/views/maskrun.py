from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from mrcnn import utils
from mrcnn.utils import extract_bboxes
from PIL import Image, ImageOps
from django.templatetags.static import static
from .variables import ID
from mainapp.models import Data
from django.core.files.base import ContentFile

import io
import json
import mrcnn
import tensorflow as tf
import mrcnn.config
import mrcnn.model
import numpy as np
import cv2
import cvzone
import os
import imutils
# import matplotlib.pyplot as plt

CLASS_NAMES = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

class SimpleConfig(mrcnn.config.Config):
    NAME = "coco_inference"
   
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    NUM_CLASSES = len(CLASS_NAMES)

model = mrcnn.model.MaskRCNN(mode="inference", 
                             config=SimpleConfig(),
                             model_dir=os.getcwd())

model.load_weights(filepath = "mask_rcnn_coco.h5", by_name=True, )

def get_box_image(img_path):
    image = Image.open(img_path)
    image = ImageOps.exif_transpose(image)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

    print("image", image.shape[0])

    r = model.detect([image], verbose=0)

    r = r[0]

    image.close()

    y1 = r["rois"][0][0]
    x1 = r["rois"][0][1]
    y2 = r["rois"][0][2]
    x2 = r["rois"][0][3]

    height = y2 - y1
    width = x2 - x1

    print("height", height )
    print("width", width)

    crop_img = image[y1:y2, x1:x2]

    r = model.detect([crop_img], verbose=0)

    r = r[0]

    person_mask = r['masks'][:, :, np.argmax(r['class_ids'] == 1)]

    
    print("person mask", person_mask.shape[0])

    person_image = np.zeros((crop_img.shape[0], crop_img.shape[1], 4), dtype=np.uint8)
  
    person_image[:, :, :3] = crop_img  # Copy the RGB channels from the original image
    
    person_image[:, :, 3] = person_mask * 255  # Set the alpha channel of the person region to 255

    print("person image", person_image.shape[0])

    bboxes = extract_bboxes(r["masks"])
    person_box = bboxes[0]

    return r, height, width, person_image, person_box

def match_height_ratio(h1, h2, realh1, realh2):
    h2 = (float(realh2)/float(realh1)) * h1
    return h2

def match_width_ratio(h1, new_h1, w1):
    calc = w1/h1
    return calc * new_h1  

def maskrun_program(id):
	print("id", id)
	data = Data.objects.get(id=id)

	person1 = data.person1
	person2 = data.person2
	realh1 = data.height1
	realh2 =  data.height2

	r1, p1_height, p1_width, crop_image1, p1_box = get_box_image(person1)
	mask1 = r1["masks"]

	r2, p2_height, p2_width, crop_image2, p2_box = get_box_image(person2)
	mask2 = r2["masks"]

	new_height = match_height_ratio(p1_height, p2_height, realh1, realh2)
	new_widht = match_width_ratio(p2_height, new_height, p2_width)

	crop_image2 = cv2.resize(crop_image2, (int(new_widht), int(new_height)))



	total_height = max(crop_image1.shape[0], crop_image2.shape[0])
	total_width = crop_image1.shape[1] + crop_image2.shape[1]
	# Create a blank canvas with the size of the combined images
	combined_image = np.zeros((int(total_height), int(total_width), 4), dtype=np.uint8)

	white_spaces = abs(crop_image1.shape[0] - crop_image2.shape[0])

	if total_height == crop_image1.shape[0]:

	    # Copy image1 to the left half of the combined image
	    combined_image[:crop_image1.shape[0], :crop_image1.shape[1]] = crop_image1

	    combined_image[white_spaces:, crop_image1.shape[1]:] = crop_image2

	elif total_height == crop_image2.shape[0]:

	    combined_image[:crop_image2.shape[0], crop_image1.shape[1]:] = crop_image2

	    combined_image[white_spaces:, :crop_image1.shape[1]] = crop_image1

	print("combined_image",combined_image.shape)



	if combined_image.shape[0] < 1000:
		combined_image = cv2.resize(combined_image, (combined_image.shape[1] + (840 - combined_image.shape[1]), combined_image.shape[0] + (1405 - combined_image.shape[0])))

	else:
		combined_image = cv2.resize(combined_image, (combined_image.shape[1] - (combined_image.shape[1] - 840), combined_image.shape[0] - (combined_image.shape[0] - 1405)))

	background = cv2.imread("background.jpg")

	print("background",background.shape)

	png_start_width = (background.shape[1]//2) - (combined_image.shape[1]//2)

	imgResult = cvzone.overlayPNG(background, combined_image, [png_start_width, 500])

	imgResult = cv2.cvtColor(imgResult, cv2.COLOR_BGR2RGB)
	# image_name = 'myimage.jpg'
	# destination_path = os.path.join('mainapp/images', image_name )  # Example: 'images/myimage.jpg'

	# static_root = 'mainapp/static'  # Replace with the actual path to your static folder
	# destination_full_path = os.path.join(static_root, destination_path)

	# success, encoded_image = cv2.imencode('.jpg', imgResult)

	pil_image = Image.fromarray(imgResult)

	# Create a BytesIO object to hold the image data
	temp_buffer = io.BytesIO()

	# Save the PIL Image object to the buffer as JPEG
	pil_image.save(temp_buffer, format='JPEG')  # Adjust the format if needed

	# Create a ContentFile from the buffer's value
	content_file = ContentFile(temp_buffer.getvalue())

	# Get the model instance
	data = Data.objects.get(id=id)  # Replace 1 with the primary key of your model instance

	# Assign the image file to the image field
	data.final_image.save(f"{id}.jpg", content_file)

	# Save the model instance
	data.save()
	# if success:
	# 	with open(destination_full_path, 'wb') as file:
	# 		file.write(encoded_image)
	# 	return JsonResponse({'message': image_name})
	# else:
	# 	return JsonResponse({'error': 'not found'}, status=404)
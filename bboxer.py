import os
import json
import cv2
import numpy as np

# Initialize the COCO-style annotations dictionary
coco_annotations = {
    "images": [],
    "annotations": [],
    "categories": []
}

# Define the categories (classes)
categories = [{'id': 1, 'name': 'cup'}, {'id': 2, 'name': 'ng'}, {'id': 3, 'name': 'other'}]
coco_annotations["categories"] = categories

# Define a function to add an image to the COCO-style annotations
def add_image(image_id, file_name, width, height):
    image = {
        "id": image_id,
        "file_name": file_name,
        "width": width,
        "height": height
    }
    coco_annotations["images"].append(image)

# Define a function to add an annotation to the COCO-style annotations
def add_annotation(annotation_id, image_id, category_id, bbox):
    annotation = {
        "id": annotation_id,
        "image_id": image_id,
        "category_id": category_id,
        "bbox": bbox,
        "area": bbox[2] * bbox[3],  # width * height
        "iscrowd": 0
    }
    coco_annotations["annotations"].append(annotation)

# Define a function to get the bounding boxes and labels for an image
def get_bounding_boxes_and_labels_for_image(filename):
    # Image is abnormal, create a bounding box around non-black region
    image = cv2.imread(os.path.join("outpic", filename))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    bounding_boxes = []
    labels = []
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        bounding_box = [x, y, w, h]
        bounding_boxes.append(bounding_box)
        labels.append(2)  # The category ID for "ng" is 2
    
    return bounding_boxes, labels

# Loop through each image in the dataset
image_id = 1
annotation_id = 1
for filename in os.listdir("outpic"):
    if filename.endswith((".png", ".jpg")) and ("ng" in filename or "other" in filename):
        # Load the image with OpenCV to get its dimensions
        image = cv2.imread(os.path.join("outpic", filename))
        height, width = image.shape[:2]

        # Check if the image is not entirely black
        if np.any(image):
            # Add the image to the COCO-style annotations
            add_image(image_id, filename, width, height)

            # Get the bounding boxes and labels for the current image
            bounding_boxes, labels = get_bounding_boxes_and_labels_for_image(filename)

            # Add each bounding box as an annotation
            for bbox, label in zip(bounding_boxes, labels):
                # Check if the bounding box is within the image dimensions
                x_min, y_min, bbox_width, bbox_height = bbox
                if x_min + bbox_width <= width and y_min + bbox_height <= height:
                    add_annotation(annotation_id, image_id, label, bbox)
                    annotation_id += 1

            image_id += 1

# Save the COCO-style annotations to a JSON file
with open("coco_annotations.json", "w") as json_file:
    json.dump(coco_annotations, json_file)

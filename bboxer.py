import os
import json
import cv2

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

# Define a function to check if a string contains a specific substring
def contains_substring(string, substring):
    return substring in string

# Define a function to get the bounding boxes and labels for an image
def get_bounding_boxes_and_labels_for_image(filename):
    # Check if the filename contains "pass" or "target"
    if contains_substring(filename, "pass") or contains_substring(filename, "target"):
        # Image is normal, return empty bounding boxes and labels
        return [], []
    else:
        # Image is abnormal, return a single bounding box and "ng" label
        image = cv2.imread(os.path.join("outpic", filename))
        height, width = image.shape[:2]
        bounding_box = [0, 0, width, height]
        labels = ["ng"]
        return [bounding_box], labels

# Loop through each image in the dataset
image_id = 1
annotation_id = 1
for filename in os.listdir("outpic"):
    if filename.endswith((".png", ".jpg")):
        # Load the image with OpenCV to get its dimensions
        image = cv2.imread(os.path.join("outpic", filename))
        height, width = image.shape[:2]

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

import json
from collections import Counter

# Load the annotations
with open('./train/cupa.json', 'r') as f:
    annotations = json.load(f)

# Initialize a counter
label_counter = Counter()

# Go through the annotations
for annotation in annotations['annotations']:
    label_counter[annotation['category_id']] += 1

# Create a mapping from category_id to category_name
category_id_to_name = {category['id']: category['name'] for category in annotations['categories']}

# Print the results
for label, count in label_counter.items():
    label_name = category_id_to_name.get(label, 'Unknown label')
    print(f"Label {label} ({label_name}) has {count} instances")

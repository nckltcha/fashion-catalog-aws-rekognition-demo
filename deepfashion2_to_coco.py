import json
import os
from PIL import Image
import numpy as np

num_images = 30000  # Number of images
sub_index = 0       # Index of ground truth instance
image_path = r'images/annotation/'  # Use raw string for correct path formatting
json_path = r'images/dataset/'
output_json_path = 'deepfashion2.json'  # Final output file

dataset = {
    "info": {},
    "licenses": [],
    "images": [],
    "annotations": [],
    "categories": []
}

# Define the category ranges expected for landmarks (assuming based on the script logic)
category_landmark_ranges = {
    1: (0, 25),
    2: (25, 58),
    3: (58, 89),
    4: (89, 128),
    5: (128, 143),
    6: (143, 158),
    7: (158, 168),
    8: (168, 182),
    9: (182, 190),
    10: (190, 219),
    11: (219, 256),
    12: (256, 275),
    13: (275, 294)
}

# Load categories here...

for num in range(1, num_images + 1):
    json_name = os.path.join(image_path, f"{str(num).zfill(6)}.json")
    image_name = os.path.join(json_path, f"{str(num).zfill(6)}.jpg")

    # Check if both the image and JSON file exist before proceeding
    if not os.path.exists(json_name) or not os.path.exists(image_name):
        print(f"File missing for image number: {num}")
        continue

    imag = Image.open(image_name)
    width, height = imag.size

    with open(json_name, 'r') as f:
        temp = json.load(f)

    pair_id = temp.get('pair_id', -1)

    dataset['images'].append({
        'coco_url': '',
        'date_captured': '',
        'file_name': f"{str(num).zfill(6)}.jpg",
        'flickr_url': '',
        'id': num,
        'license': 0,
        'width': width,
        'height': height
    })

    for key, value in temp.items():
        if key in ['source', 'pair_id']:
            continue
        
        # Prepare empty points array
        points = np.zeros(294 * 3)
        sub_index += 1  # Increment sub_index with each annotation

        box = value.get('bounding_box', [0, 0, 0, 0])
        w, h = box[2] - box[0], box[3] - box[1]
        x_1, y_1 = box[0], box[1]
        bbox = [x_1, y_1, w, h]

        cat = value.get('category_id', -1)
        style = value.get('style', 0)
        seg = value.get('segmentation', [])
        landmarks = value.get('landmarks', [])

        # Ensure landmarks length is appropriate for the category
        if cat not in category_landmark_ranges:
            print(f"Unknown category {cat} for image number {num}")
            continue

        start_idx, end_idx = category_landmark_ranges[cat]
        required_points = end_idx - start_idx

        # Check if landmarks have enough data points
        if len(landmarks) < required_points * 3:
            print(f"Landmark data insufficient for image {num}, category {cat}")
            continue  # Skip this annotation if data is insufficient

        points_x = landmarks[0::3]
        points_y = landmarks[1::3]
        points_v = landmarks[2::3]

        # Only fill in as many landmarks as available
        for idx in range(start_idx, min(end_idx, len(points_x))):
            n = idx - start_idx
            points[3 * idx] = points_x[n]
            points[3 * idx + 1] = points_y[n]
            points[3 * idx + 2] = points_v[n]

        num_points = int(np.sum(np.array(points_v[:required_points]) > 0))

        dataset['annotations'].append({
            'area': w * h,
            'bbox': bbox,
            'category_id': cat,
            'id': sub_index,
            'pair_id': pair_id,
            'image_id': num,
            'iscrowd': 0,
            'style': style,
            'num_keypoints': num_points,
            'keypoints': points.tolist(),
            'segmentation': seg,
        })

# Write the final dataset JSON file
with open(output_json_path, 'w') as f:
    json.dump(dataset, f)

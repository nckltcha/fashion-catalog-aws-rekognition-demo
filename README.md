# Rekognition-demo

AWS Rekognition demo, using some images of the DeepFashion2 dataset.

# How to use



## `S3`

  - Create a S3 bucket
  - Upload all images in the S3

## `Build`

 - Change the s3_bucket_name in coco_to_manifest.py
 - Run python deepfashion2_to_coco.py to create the coco file.
 - Run python coco_to_manifest.py to create the manifest file and upload the S3

## `Train`

  - Create a AWS Rekognition Model using the .manifest
  - Start model training

## `Usage`


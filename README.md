# Rekognition-demo

AWS Rekognition demo, using some images of the DeepFashion2 dataset.

# How to use

  To use the model we need a s3 bucket setup with all the images, then follow the building order using the python scripts, after the manifest file uploaded in the s3 the AWS Rekognition Custom Label model should be created using it, then it`s ready to use.

  To test use the model the images used should be in a s3 bucket.


## `S3`

  - Create a S3 bucket
  - Upload all images in the S3 using the path "images/"

  for convenience we used this schema for the bucket :

  ![s3_schema](S3.jpg)

## `Build`

 - Change the s3_bucket_name in coco_to_manifest.py.

 - Run to create the coco file:
  ```
    python coco_to_manifest.py
  ```

 - Run to create the manifest file and upload the S3:
  ```
    python coco_to_manifest.py
  ```

## `Train`

  - Create a AWS Rekognition Custom Label Model using the .manifest.
  - Start model training.

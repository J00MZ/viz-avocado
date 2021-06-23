# viz-avocado
This repo will build and push an image of Avocado Goodness 🥑🥑 to S3  
The image will run a python script that triggers when a file is uploaded to the S3 Bucket `avocado-file-toaster` and will send the file type and URI to the new object in S3 to an email address

## Triggering the Lambda Function

- Upload an object to `s3://viz-avocado`

## Building the Docker Image
- Push code to `master` branch.  

Will trigger:  
1. New Docker build of the image
2. Push built image to ECR
3. Run a Deployment of the new container from ECR to Lambda

# viz-avocado
This repo will build and push an image of Avocado Goodness 🥑🥑 to S3  
The image will run a python script that triggers when a file is uploaded to the S3 Bucket `avocado-file-toaster` and will send the file type and URI to the new object in S3 to an email address

## Triggering the Lambda Function

- Upload an object to `s3://viz-avocado`

## Building the Docker Image
Currently the process builds including the runtime for lambda in every image.  
This results in images that are large in size due to the whole of Lambda runtime baked in.  
A possible workaround suggested by AWS is to mount the Lambda runtime as a volume on every container function invocation

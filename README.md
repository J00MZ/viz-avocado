# viz-avocado
- This repo will build and push an image of Avocado Goodness to [AWS ECR](https://aws.amazon.com/ecr/) 🥑🥑  
- The image is containerized in an [AWS Lambda](https://aws.amazon.com/lambda/) function
- The Function consists of a Python script that triggers when a file is uploaded to the S3 Bucket `avocado-file-toaster`  
- When function is triggered, it will send the file type and S3 URI of the new object in S3 to an email address using [AWS SES](https://aws.amazon.com/ses/)

# Usage
## Triggering Lambda Function

- Upload an object to `s3://viz-avocado`

## Building the Docker Image
- Push application or CI workflow code to `main` branch.  

Will trigger:  
1. New Docker build of the image
2. Push newly built image to ECR
3. Run a Deployment of the new container from ECR to the Lambda Function

## CI
Runs with [GitHub Actions](https://github.com/J00MZ/viz-avocado/actions)

# Initial Setup

1. Created the S3 bucket
2. Created ECR Repo to push Docker image to
3. Created IAM role for Lambda to assume with permissions
4. Created the Lambda Function to use the ECR Repo created at step `2`.
5. Added secrets used by CI to access AWS to GitHub Repo [secrets](https://github.com/J00MZ/viz-avocado/settings/secrets/actions)
6. Added email addresses to SES for authorization and approved via link sent to emails
7. Added email addresses as environment variables to Lambda

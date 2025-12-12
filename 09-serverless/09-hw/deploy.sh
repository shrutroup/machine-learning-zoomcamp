#!/bin/bash

IMAGE_NAME="hair-classifier-lambda"
AWS_REGION="us-west-2"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity | jq -r ".Account")
ECHO "AWS ACCOUNT ID: ${AWS_ACCOUNT_ID}"

# Get latest commit SHA and current datetime
COMMIT_SHA=$(git rev-parse --short HEAD)
DATETIME=$(date +"%Y%m%d-%H%M%S")
IMAGE_TAG="${COMMIT_SHA}-${DATETIME}"

ECR_URI=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
IMAGE_URI="${ECR_URI}/${IMAGE_NAME}:${IMAGE_TAG}"
ECHO "IMAGE_URI ${IMAGE_URI}"

# Check if repository exists, create if it doesn't
if ! aws ecr describe-repositories \
  --repository-names ${IMAGE_NAME} \
  --region ${AWS_REGION} \
  >/dev/null 2>&1; then
  echo "Creating ECR repository: ${IMAGE_NAME}"
  aws ecr create-repository \
    --repository-name ${IMAGE_NAME} \
    --region ${AWS_REGION}
else
  echo "ECR repository ${IMAGE_NAME} already exists"
fi


aws ecr get-login-password \
  --region ${AWS_REGION} \
| docker login \
  --username AWS \
  --password-stdin ${ECR_URI}

docker build --platform linux/amd64 --provenance false -t  ${IMAGE_NAME}:${IMAGE_TAG} .
docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_URI}
docker push ${IMAGE_URI}

echo "Image pushed successfully!"
echo "Use this URI in Lambda: ${IMAGE_URI}"
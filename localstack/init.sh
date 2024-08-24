#!/bin/bash

sleep 5  # Add a delay to ensure services are up

echo "Creating S3 bucket..."
awslocal s3 mb s3://uploads
awslocal s3 mb s3://processed

echo "Creating queues..."
awslocal sqs create-queue --queue-name processing-queue
awslocal sqs create-queue --queue-name embedding-queue

echo "Initialization complete."
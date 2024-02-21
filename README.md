# AWS Lambda Function to Collect VPC Information and Store in AWS S3 Bucket

## Overview
This code defines an AWS Lambda function that retrieves information about all VPCs and subnets in an AWS account and stores the data in a JSON format in an S3 bucket.

The code uses the Boto3 library to interact with AWS services. The function starts by initializing an EC2 client and then retrieves all VPCs in the account using the describe_vpcs() function. For each VPC, it retrieves all the subnets in that VPC using the describe_subnets() function. The VPC and subnet information is then stored in a Python dictionary.

The code then uses the Boto3 S3 resource to upload the VPC information to an S3 bucket. The S3 key name for the file is dynamically generated based on the current timestamp.

Finally, the function returns a response with a 200 status code and a message indicating that the VPC information has been successfully dumped to the S3 bucket.


## Usage
To use this code, create an AWS Lambda function with the lambda_handler function as the entry point. Ensure that the Lambda function has permission to access the necessary AWS services such as EC2 and S3. Also, replace the {mybucketname} placeholder with the name of the S3 bucket where you want to store the VPC .



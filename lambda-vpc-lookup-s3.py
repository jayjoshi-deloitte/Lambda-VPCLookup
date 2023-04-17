import boto3
import json

def lambda_handler(event, context):
    # Set up S3 client
    s3 = boto3.client('s3')
    bucket_name = "target"
    
    # Set up IAM client to list all accounts
    iam = boto3.client('iam')
    account_list = iam.list_account_aliases()['AccountAliases']
    
    # Set up EC2 client to retrieve VPC details
    ec2 = boto3.client('ec2')
    
    # Loop through all accounts and retrieve VPC details
    for account in account_list:
        # Assume role in account
        sts = boto3.client('sts')
        assumed_role_object = sts.assume_role(RoleArn='arn:aws:iam::' + account + ':role/RoleName', RoleSessionName="AssumeRoleSession1")
        credentials = assumed_role_object['Credentials']
        ec2 = boto3.client('ec2', aws_access_key_id=credentials['AccessKeyId'],
                            aws_secret_access_key=credentials['SecretAccessKey'],
                            aws_session_token=credentials['SessionToken'])
        
        # Retrieve VPC details
        response = ec2.describe_vpcs()
        
        # Dump VPC details to S3
        for vpc in response['Vpcs']:
            key_name = 'account-' + account + '-vpc-' + vpc['VpcId'] + '.json'
            s3.put_object(Bucket=bucket_name, Key=key_name, Body=json.dumps(vpc))
    
    return {
        'statusCode': 200,
        'body': json.dumps('VPC details dumped successfully to S3!')
    }

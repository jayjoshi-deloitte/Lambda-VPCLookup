import boto3
import json
import datetime

def lambda_handler(event, context):
    
    # Define a list to store the VPC information
    vpc_info = []
    
    # Initialize an EC2 client using the temporary credentials
    ec2 = boto3.client('ec2')
        
    # Retrieve all VPCs in the account
    response = ec2.describe_vpcs()
        
    # Loop through each VPC in the response
    for vpc in response['Vpcs']:
        vpc_id = vpc['VpcId']
        vpc_cidr = vpc['CidrBlock']
        vpc_tags = vpc.get('Tags', [])
            
        # Retrieve all subnets in the VPC
        subnet_response = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
        subnets = []
            
        # Loop through each subnet in the response
        for subnet in subnet_response['Subnets']:
            subnet_id = subnet['SubnetId']
            subnet_cidr = subnet['CidrBlock']
            subnet_tags = subnet.get('Tags', [])
                
            subnets.append({
                'id': subnet_id,
                'cidr': subnet_cidr,
                'tags': subnet_tags
            })
            
        vpc_info.append({
            'id': vpc_id,
            'cidr': vpc_cidr,
            'tags': vpc_tags,
            'subnets': subnets
        })
    
    # Dump the VPC information to an S3 bucket
    bucket_name = '{mybucketname}'
    s3_key = 'vpc_info_{}.json'.format(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    
    s3 = boto3.resource('s3')
    object = s3.Object(bucket_name, s3_key)
    object.put(Body=json.dumps(vpc_info))
    
    return {
        'statusCode': 200,
        'body': json.dumps('VPC information dumped to S3 bucket!')
    }

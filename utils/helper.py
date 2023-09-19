import boto3

import redshift_connector as rdc

region = 'us-east-2'

def create_bucket(access_key, secret_key, bucket_name):
    client = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': region
        }
    )
    
    
def connect_to_dwh(conn_details):
    return rdc.connect(**conn_details)
    
    
    
    

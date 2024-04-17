import boto3
from datetime import datetime, timedelta, UTC

# Set your AWS credentials
aws_access_key_id = ""
aws_secret_access_key = ""

# Set the S3 bucket name
bucket_name = 'linthr-dev-db-backups'

# Create an S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# Set the number of days to keep the folders
days_to_keep = 5

# Calculate the cutoff date
cutoff_date = datetime.now(UTC) - timedelta(days=days_to_keep)

# List all the files in the bucket
response = s3.list_objects_v2(Bucket=bucket_name, Prefix='')

# # Delete the file that are older than the cutoff date
for content in response.get('Contents', []):
    key = content['Key']
    last_modified = content['LastModified']
    print(last_modified, cutoff_date)
    if last_modified < cutoff_date:
        print(f'Deleting file: {key}')
        s3.delete_object(Bucket=bucket_name, Key=key)

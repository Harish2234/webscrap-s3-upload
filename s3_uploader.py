import boto3
import json
from botocore.exceptions import ClientError

# Initialize the S3 client
s3_client = boto3.client('s3', region_name='ap-southeast-2')

# Define the bucket name and object key
bucket_name = 'bucketstatic'
object_key = 'index.html'


def empty_bucket(bucket_name):
    """Empty the specified S3 bucket by deleting all its objects."""
    try:
        bucket_objects = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in bucket_objects:
            for obj in bucket_objects['Contents']:
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
            print(f'Bucket {bucket_name} has been emptied.')
        else:
            print(f'Bucket {bucket_name} is already empty.')
    except ClientError as e:
        print(f"Error while emptying the bucket: {e}")
        raise

def create_or_clear_bucket(bucket_name):
    """Check if the bucket exists. If it exists, delete it. Otherwise, create a new one."""
    try:
        # Check if the bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        print(f'Bucket {bucket_name} already exists. Deleting it...')
        
        # Delete all objects in the bucket
        empty_bucket(bucket_name)
        
        # Delete the bucket itself
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f'Bucket {bucket_name} deleted.')

    except ClientError as error:
        # If the bucket doesn't exist, handle the error by creating a new one
        if error.response['Error']['Code'] == '404':
            print(f'Bucket {bucket_name} does not exist. Creating a new one...')
        else:
            print(f"Error checking bucket: {error}")
            raise

    # Create a new bucket
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-southeast-2'
            }
        )
        print(f'Bucket {bucket_name} created successfully')
    except ClientError as e:
        print(f"Error creating bucket: {e}")
        raise

def configure_bucket(bucket_name):
    """Configure the S3 bucket for public access, add policy, and enable static hosting."""
    try:
        # Disable public access block settings
        s3_client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )
        print(f'Public access block settings disabled for {bucket_name}')

        # Set bucket policy to allow public-read
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }

        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(bucket_policy)
        )
        print(f'Bucket policy set to allow public read access for {bucket_name}')

        # Enable static website hosting
        website_configuration = {
            'IndexDocument': {'Suffix': 'index.html'},
            'ErrorDocument': {'Key': 'error.html'}  # Optional: configure an error document if desired
        }

        s3_client.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration=website_configuration
        )
        print(f'Static website hosting enabled for {bucket_name}')
    except ClientError as e:
        print(f"Error configuring bucket: {e}")
        raise

def upload_file(bucket_name, object_key):
    """Upload the HTML file to the bucket with the correct MIME type."""
    try:
        s3_client.upload_file(
            'E:\\pyt\\python\\boto3task\\webscrap\\index.html', bucket_name, object_key,
            ExtraArgs={'ContentType': 'text/html',
                       'CacheControl': 'no-cache, no-store, must-revalidate'}
        )
        print('File uploaded successfully with ContentType set to text/html')
    except ClientError as upload_error:
        print(f'File upload error: {upload_error}')
        raise

def get_website_url(bucket_name, object_key):
    """Generate and print the website URL for the uploaded file."""
    line_length = 100
    for _ in range(line_length):
        print('$', end='')
    print() 
    region = 'ap-southeast-2'
    website_url = f'http://{bucket_name}.s3-website-{region}.amazonaws.com/{object_key}'
    print(f'Your website is available at: {website_url}')

# Main execution flow
def main():
    """Main function to handle bucket creation, configuration, and file upload."""
    print_star_line()  # Print star line at the beginning
    try:
        create_or_clear_bucket(bucket_name)
        configure_bucket(bucket_name)
        upload_file(bucket_name, object_key)
        get_website_url(bucket_name, object_key)
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()

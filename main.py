from requesters import fetch_and_save_html
from s3_uploader import create_or_clear_bucket, configure_bucket, upload_file, get_website_url

def main():
    """Main function to fetch HTML content, save it, and upload it to S3."""
    url = 'https://sololearn.com/en/'
    file_path = 'index.html'
    
    # Fetch and save HTML content
    fetch_and_save_html(url, file_path)
    
    # Define S3 bucket name and object key
    bucket_name = 'bucketstatic'
    object_key = 'index.html'
    
    try:
        # Create or clear S3 bucket
        create_or_clear_bucket(bucket_name)
        
        # Configure S3 bucket
        configure_bucket(bucket_name)
        
        # Upload the HTML file to the bucket
        upload_file(bucket_name, object_key)
        
        # Get and print the website URL
        get_website_url(bucket_name, object_key)
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()

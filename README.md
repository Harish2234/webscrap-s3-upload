# Web Scraper and AWS S3 Uploader

## Project Description
This project is a Python-based tool that automates the process of web scraping and uploading HTML content to AWS S3 for static website hosting. It consists of three modules:

1. **`main.py`:** 
   - This is the entry point of the project, which fetches the HTML content from a specified URL and saves it locally.
   
2. **`requesters.py`:**
   - This module handles the HTTP request to fetch the HTML content from a given URL and saves it to a specified local file path.

3. **`s3_uploader.py`:**
   - This module is responsible for uploading the scraped HTML file to an AWS S3 bucket.
   - It also handles bucket creation, emptying existing buckets, configuring public access, and enabling static website hosting.

## Key Features
- **Web Scraping**: Automatically fetches HTML content from a provided URL.
- **AWS S3 Integration**: Uploads files to an S3 bucket, with options for public read access and static website hosting.
- **Bucket Management**: Handles bucket creation, emptying, and policy configuration to ensure seamless file uploads.
- **Static Website Hosting**: Configures the S3 bucket to host the uploaded HTML content as a static website.

## Technologies Used
- **Python**: For scripting the web scraping and S3 interactions.
- **Boto3**: AWS SDK for Python, used for S3 interactions.
- **Requests**: For making HTTP requests to fetch the HTML content.

## How to Run
1. Install the required dependencies using `pip`:
   ```bash
   pip install boto3 requests

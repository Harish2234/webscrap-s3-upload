import requests

def fetch_and_save_html(url, file_path):
    """Fetches HTML content from a URL and saves it to a file."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"HTML content from {url} saved to {file_path}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

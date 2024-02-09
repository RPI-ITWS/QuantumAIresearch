from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def get_book_links():
    # URL for the Gutenberg Index API
    url = 'https://gutendex.com/books/'
    
    try:
        # Make a GET request to the API
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Extract links for specified content types
            links = {}
            for book in data.get('results', []):
                book_id = book['id']
                book_formats = book.get('formats', {})
                
                # Extract links for text/plain; charset=us-ascii and text/plain; charset=utf-8
                ascii_link = book_formats.get('text/plain; charset=us-ascii', None)
                utf8_link = book_formats.get('text/plain; charset=utf-8', None)
                
                # Add links to the dictionary
                links[book_id] = {'ascii': ascii_link, 'utf8': utf8_link}
            
            return links
        else:
            # Print an error message with status code if the request was unsuccessful
            print(f'Error: Unable to retrieve book links. Status Code: {response.status_code}')
            return {}
    except requests.exceptions.RequestException as e:
        # Print an error message if there's a request exception
        print(f'Error: {e}')
        return {}

def download_text_files(url, output_dir):
    print(f"Downloading text files from: {url}")
    # Send a GET request to the URL with streaming enabled
    with requests.get(url, stream=True) as response:
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all anchor tags
            links = soup.find_all('a')
            
            # Create the output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Download text files with ASCII encoding
            for link in links:
                href = link.get('href')
                if href and href.endswith('.txt') and 'charset=us-ascii' in href:
                    file_url = urljoin(url, href)
                    file_name = os.path.join(output_dir, os.path.basename(href))
                    
                    # Stream download the file content
                    with requests.get(file_url, stream=True) as file_response:
                        with open(file_name, 'wb') as file:
                            for chunk in file_response.iter_content(chunk_size=8192):
                                file.write(chunk)
                    print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to download files from {url}. Status Code: {response.status_code}")

if __name__ == '__main__':
    book_links = get_book_links()
    downloaded_files = False  # Flag to indicate if any files were downloaded
    
    if book_links:
        print("Links for specified content types:")
        for book_id, links in book_links.items():
            if links['ascii']:  # Ensure there is a link before attempting to download
                url = links['ascii']
                output_dir = r'C:\Users\aanya\TEXTQTM'
                download_text_files(url, output_dir)
                
                # Check if any files were downloaded
                if os.listdir(output_dir):
                    downloaded_files = True
    else:
        print("No book links found.")
    
    if downloaded_files:
        print("Files were downloaded successfully.")
    else:
        print("No files were downloaded.")

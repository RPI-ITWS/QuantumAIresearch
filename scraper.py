import requests

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

if __name__ == '__main__':
    book_links = get_book_links()
    
    if book_links:
        print("Links for specified content types:")
        for book_id, links in book_links.items():
            print(f"Book ID: {book_id}")
            print(f"Ascii Link: {links['ascii']}")
            print(f"UTF-8 Link: {links['utf8']}")
            print()
    else:
        print("No book links found.")

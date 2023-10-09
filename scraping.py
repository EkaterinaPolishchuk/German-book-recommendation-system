import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://einfachebuecher.de/Buecher/?order=name-asc&p=&properties=6c06d8d1d3a34412b2110d42d43d7638"
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'accept': '*/*'
}
HOST = 'https://einfachebuecher.de/'

def fetch_html(url, page=1):
    """
    Fetch HTML content from a given URL.
    Args:
        url (str): The URL to fetch.
        page (int, optional): The page number (default is 1).

    Returns:
        requests.Response: The HTTP response containing the HTML content.
    """
    try:
        response = requests.get(url, headers=HEADERS, params={"p": page}, timeout=100)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching HTML: {e}")
        return None

def extract_books(html):
    """
    Extract book names, image and descriptions from HTML.

    Args:
        html (str): The HTML to parse.

    Returns:
        pd.DataFrame: A DataFrame containing book names, images and descriptions.
    """
    soup = BeautifulSoup(html, 'html.parser')

    books_df = pd.DataFrame(columns=["name","image","description"])
    names = []
    descriptions = []
    images = []

    for name_element in soup.find_all(class_="product-name"):
        name = name_element.get_text(strip=True)
        names.append(name)
    
    for image_element in soup.find_all(class_="product-image-wrapper"):
        images.append(image_element.a.img["src"])

    for description_element in soup.find_all(class_="product-description"):
        description = description_element.get_text(strip=True)
        descriptions.append(description)

    books_df["name"] = names
    books_df["image"] = images
    books_df["description"] = descriptions
    return books_df

def scrape_pages(num_pages=2):
    """
    Scrape book data from multiple pages.

    Args:
        num_pages (int, optional): The number of pages to scrape (default is 2).

    Returns:
        pd.DataFrame: A DataFrame containing book names, images and descriptions from multiple pages.
    """
    all_books = pd.DataFrame(columns=["name", "image", "description"])
    for page_number in range(1, num_pages + 1):
        html = fetch_html(BASE_URL, page_number)
        if html:
            page_books = extract_books(html)
            all_books = pd.concat([all_books, page_books], ignore_index=True)
        else:
            print('Error')
    return all_books

if __name__ == "__main__":
    scraped_books = scrape_pages(10)
    # scraped_books.to_csv(r'\scraped_books.csv', index=False, header=True)
    
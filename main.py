# -*- coding: utf-8 -*-
"""learning web scraping

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1C9-a6-wIYYW2pGsRGdXB2Z1zQLBoNkQV

# **Goal To Acheive**



*   Website have 50 pages and on each page theres 20 products.
*   Main goal is to access all 50 pages through loop and get all products on each page.
*   Get details: Product name, product price, url, and stock available.
*
"""

# installing required libraries.

pip install requests beautifulsoup4

#importing libraries/modules.

import requests
import re
import csv
from bs4 import BeautifulSoup

#this is the base url when we loop through different page numbers this will be base url and then page number.

base_url = "https://books.toscrape.com/catalogue/page-{}.html"

#empty list to store all products.

all_products = []

# Loop through all pages from 1 to 50 to scrape data.
for page_num in range(1, 51):
    # Format the base URL with the current page number and store it in the variable.
    page_url = base_url.format(page_num)

    # Download the page content using the requests library and parse it with BeautifulSoup.
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the main parent tag 'ol' which contains a list of products for each page.
    # The class 'row' helps to locate the specific 'ol' tag with the products.
    ol_tags = soup.find_all('ol', class_='row')

    # Iterate through each 'ol' tag to access all 'li' tags inside it.
    for ol in ol_tags:
        # Find all 'li' tags inside the 'ol' tag, each representing a product.
        li_tags = ol.find_all('li')

        # Iterate through each 'li' tag to extract necessary product details.
        for li in li_tags:
            # Find the 'h3' tag, then the 'a' tag inside it to extract the product name.
            product_name = li.find('h3').find('a').get_text(strip=True)

            # Find the 'p' tag with class 'price_color' to get the product price.
            product_price = li.find('p', class_='price_color').get_text(strip=True)

            # Find the 'a' tag inside the 'h3' to get the relative URL of the product.
            product_url_tag = li.find('h3').find('a')
            # Construct the full product URL by appending the relative URL to the base URL.
            # If there's no 'a' tag, set the URL as 'No URL'.
            product_url = "https://books.toscrape.com/catalogue/" + product_url_tag['href'] if product_url_tag else 'No URL'

            # Send a request to the individual product page to get more details.
            product_response = requests.get(product_url)
            product_soup = BeautifulSoup(product_response.text, 'html.parser')

            # Find the 'p' tag with class 'instock availability' to get stock information.
            # Extract and clean up the text to get the stock availability details.
            stock_availability = product_soup.find('p', class_='instock availability').get_text(strip=True)

            # Use a regular expression to find the first number in the stock availability text.
            # This will extract the quantity of stock available.
            stock_number = re.search(r'\d+', stock_availability).group() if stock_availability else 'No stock info'

            # Create a dictionary with the extracted product details.
            product_details = {
                'Product Name': product_name,
                'Product Price': product_price,
                'Product URL': product_url,
                'Stock Availability': stock_number
            }

            # Add the dictionary to the list of all products.
            all_products.append(product_details)



# Define the CSV file path
csv_file_path = "books_data.csv"

# Define the fieldnames (keys from the product details dictionary)
fieldnames = ["Product Name", "Product Price", "Product URL", "Stock Availability"]

# Write data to CSV
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_products)

print(f"Data saved to {csv_file_path}")

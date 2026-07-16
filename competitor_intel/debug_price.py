import cloudscraper
from bs4 import BeautifulSoup

url = "https://www.phoneplacekenya.com/product-category/smartphones/"

# Bypass bot protection
scraper = cloudscraper.create_scraper()
response = scraper.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the first product wrapper
    first_product = soup.find("div", class_="product-wrapper")

    if first_product:
        print("\n--- LIVE HTML OF THE FIRST PRODUCT ----\n")
        # print the first 1500 characters of the product's HTML
        print(first_product.prettify()[:1500])
        print("\n -------------- \n")
    else:
        print("Could not find 'product-wrapper'. The site structure may have changed")
else:
    print(f"Failed to connect. Status code: {response.status_code}")
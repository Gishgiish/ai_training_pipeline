import scrapy
import re

class PhoneplaceSpider(scrapy.Spider):
    """
    Spider to extract smartphone data from Phoneplace Kenya. 
    With Fallback selectors and regex safety nets for future proofing.
    """

    name = "phoneplace"
    allowed_domains = ["phoneplacekenya.com"]
    start_urls = ["https://www.phoneplacekenya.com/product-category/smartphones/"] # Added trailing slash to match the 301 redirect

    def parse(self, response):
        # Find all product containers on the page
        for product in response.css("div.product-wrapper"):

            # 1. Extract product name
            # Renamed local variable to 'product_name' to avoid shadowing the class attribute 'name'
            name_selectors = [
                "h3.heading-title.product-name a::text",
                "h2.woocommerce-loop-product__title a::text",
                "a.woocommerce-loop-product__link::text" # Fixed: removed redundant 'a' at the end
            ]
            product_name = None
            for selector in name_selectors:
                product_name = product.css(selector).get()
                if product_name and product_name.strip():
                    break

            # 2. Extract and clean price
            price_selectors = [
                "span.price::text",
                "span.price bdi::text",
                "span.woocommerce-Price-amount::text" # Fixed typo: was "pan."
            ]
            raw_price = None
            for selector in price_selectors:
                raw_price = product.css(selector).get()
                # FIXED: Check if raw_price exists BEFORE calling .strip() to prevent AttributeError
                if raw_price and raw_price.strip():
                    break

            # Regex Fallback to search for "Ksh" + numbers when selectors fail
            if not raw_price or not raw_price.strip():
                # FIXED: product.get_text() is not a valid Scrapy method. 
                # Use xpath("string(.)") to safely extract all visible text from the container.
                card_text = product.xpath("string(.)").get() or ""
                match = re.search(r'(?:Ksh|KES)\s*([\d,]+)', card_text, re.IGNORECASE)
                if match:
                    raw_price = match.group(0)

            # Clean the price to remove non-numeric characters (except decimals)
            clean_price = None
            if raw_price:
                clean_price = re.sub(r'[^\d.]', '', raw_price)

            # 3. Extract link and make it absolute
            link_selectors = [
                "h3.heading-title.product-name a::attr(href)",
                "a.woocommerce-loop-product__link::attr(href)"
            ]
            raw_link = None
            for selector in link_selectors:
                raw_link = product.css(selector).get()
                if raw_link:
                    break

            full_link = response.urljoin(raw_link) if raw_link else None
            
            # 4. Yield the dictionary to the Scrapy Pipeline
            yield {
                "product_name": product_name.strip() if product_name else None,
                "price": float(clean_price) if clean_price else None, # Bonus: Convert to float for your Pydantic model
                "source_url": full_link,
                "source_brand": "Phoneplace"
            }
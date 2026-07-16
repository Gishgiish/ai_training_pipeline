import scrapy
import re

class SamsungSpider(scrapy.Spider):
    """
    Playwright-enabled spider to extract smartphone data from Avechi Kenya.
    Selectors verified against live site HTML structure.
    """
    name = "samsung"
    allowed_domains = ["avechi.co.ke"]
    start_urls = ["https://avechi.co.ke/product-category/samsung/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={"playwright": True} 
            )

    def parse(self, response):
        # 1. Target the exact container class used by this theme
        for product in response.css("div.product-wrapper"):
           
            # 2. Extract Product Name
            name = product.css("h3.heading-title.product-name a::text").get()
           
            # 3. Extract and Clean Price
            # The price is nested inside span.price -> bdi
            raw_price = product.css("span.price bdi::text").get()
            clean_price = None
            
            if raw_price:
                # Remove everything except digits and dots (e.g., "KSh18,999.00" -> "18999.00")
                clean_price = re.sub(r'[^\d.]', '', raw_price)
               
            # 4. Extract Link and make it absolute
            raw_link = product.css("h3.heading-title.product-name a::attr(href)").get()
            full_link = response.urljoin(raw_link) if raw_link else None

            # 5. Yield the dictionary to the Scrapy Pipeline
            # Guard clause ensures we only yield if we actually found a product name
            if name and name.strip():
                yield {
                    "product_name": name.strip(),
                    "price": float(clean_price) if clean_price else None,
                    "source_url": full_link,
                    "source_brand": "Avechi Kenya"
                }
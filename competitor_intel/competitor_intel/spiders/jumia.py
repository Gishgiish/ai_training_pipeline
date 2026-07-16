import scrapy
import re

class JumiaSpider(scrapy.Spider):
    """
    Playwright-enabled spider to extract smartphone data from Jumia Kenya.
    Uses Jumia's specific, stable HTML class names.
    """
    name = "jumia"
    allowed_domains = ["jumia.co.ke"]
    start_urls = ["https://www.jumia.co.ke/mobile-phones/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                # Playwright is CRITICAL for Jumia due to heavy JavaScript lazy-loading
                meta={"playwright": True}
            )

    def parse(self, response):
        # 1. Target Jumia's specific product container class
        # We use both 'article.prd' and 'div.prd' to catch any theme variations
        for product in response.css("article.prd, div.prd"):
           
            # 2. Extract Product Name
            name = product.css("h3.name::text").get()
           
            # 3. Extract and Clean Price
            # Jumia wraps the price in a div with class 'prc'
            raw_price = product.css("div.prc::text").get()
            clean_price = None
            
            if raw_price:
                # Remove everything except digits and dots (e.g., "KSh 15,000" -> "15000")
                clean_price = re.sub(r'[^\d.]', '', raw_price)
               
            # 4. Extract Link and make it absolute
            # Jumia uses the class 'core' for the main product link
            raw_link = product.css("a.core::attr(href)").get()
            full_link = response.urljoin(raw_link) if raw_link else None

            # 5. Yield the dictionary to the Scrapy Pipeline
            # Guard clause ensures we only yield if we actually found a product name
            if name and name.strip():
                yield {
                    "product_name": name.strip(),
                    "price": float(clean_price) if clean_price else None,
                    "source_url": full_link,
                    "source_brand": "Jumia Kenya"
                }
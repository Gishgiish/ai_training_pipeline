import pytest
from scrapy.http import HtmlResponse

# Import the spider
from competitor_intel.spiders.samsung import SamsungSpider

def test_samsung_spider_extracts_data():
    """Test that the spider correctly parses a mock Avechi Kenya product card."""
   
    # 1. Create a fake snippet of HTML mimicking the ACTUAL Avechi Kenya structure
    mock_html = """
    <html><body>
        <div class="product-wrapper">
            <h3 class="heading-title product-name">
                <a href="/product/samsung-galaxy-s24-ultra-256gb">Galaxy S24 Ultra 5G</a>
            </h3>
            <div class="product-price">
                <span class="price">
                    <bdi>KSh 189,999.00</bdi>
                </span>
            </div>
        </div>
    </body></html>
    """
   
    # 2. Create a fake Scrapy Response object with the correct base URL
    url = "https://avechi.co.ke/product-category/samsung/"
    response = HtmlResponse(url=url, body=mock_html, encoding='utf-8')
   
    # 3. Instantiate our spider
    spider = SamsungSpider()
   
    # 4. Call the spider's parse method
    results = list(spider.parse(response))
   
    # 5. Assert that we got exactly one item back
    assert len(results) == 1
   
    # 6. Assert the extracted data is exactly what we expect
    extracted_item = results[0]
    
    # Name should be cleanly stripped
    assert extracted_item["product_name"] == "Galaxy S24 Ultra 5G"
    
    # Price should be a FLOAT now (because of float(clean_price) in the spider)
    assert extracted_item["price"] == 189999.00 
    
    # URL should be properly joined to the base URL
    assert extracted_item["source_url"] == "https://avechi.co.ke/product/samsung-galaxy-s24-ultra-256gb"
    
    # Brand should reflect the actual source
    assert extracted_item["source_brand"] == "Avechi Kenya"
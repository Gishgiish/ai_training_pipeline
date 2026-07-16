import pytest
from scrapy.http import HtmlResponse

# Import the spider (we will name it JumiaSpider)
from competitor_intel.spiders.jumia import JumiaSpider

def test_jumia_spider_extracts_data():
    """Test that the spider correctly parses a mock Jumia product card."""
   
    # 1. Create a fake snippet of HTML mimicking Jumia's structure
    mock_html = """
    <html><body>
        <article class="prd">
            <a href="/samsung-galaxy-s24-5g.html" class="core">
                <h3 class="name">Samsung Galaxy S24 5G - 128GB ROM + 8GB RAM</h3>
            </a>
            <div class="prc>
                <span>KSh 149,999</span>
            </div>
        </article>
    </body></html>
    """
   
    # 2. Create a fake Scrapy Response object
    url = "https://www.jumia.co.ke/mobile-phones/"
    response = HtmlResponse(url=url, body=mock_html, encoding='utf-8')
   
    # 3. Instantiate our spider
    spider = JumiaSpider()
   
    # 4. Call the spider's parse method
    results = list(spider.parse(response))
   
    # 5. Assert that we got exactly one item back
    assert len(results) == 1
   
    # 6. Assert the extracted data is exactly what we expect
    extracted_item = results[0]
    assert extracted_item["product_name"] == "Samsung Galaxy S24 5G - 128GB ROM + 8GB RAM"
    assert extracted_item["price"] == "149999" # Cleaned price
    assert extracted_item["source_url"] == "https://www.jumia.co.ke/samsung-galaxy-s24-5g.html.html"
    assert extracted_item["source_brand"] == "Jumia Kenya"
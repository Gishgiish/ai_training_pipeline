import pytest
from scrapy.http import HtmlResponse

from competitor_intel.spiders.phoneplace import PhoneplaceSpider

def test_phoneplace_spider_extracts_data():
    """Test that the spider correctly parses a mock Phoneplace product card."""

    # 1. Create a fake HTML snippet
    mock_html = """
    <html><body>
        <div class="product-wrapper">
            <h3 class="heading-title product-name">
                <a href="/product/samsung-galaxy-s23/">Samsung Galaxy S23 Ultra</a>
            <h3>
            <span class="price">Ksh 185,000</span>
        </div>
    </body></html>
    """

    # 2. Create a fake Scrapy response object
    url = "https://www.phoneplacekenya.com/product-category/smartphoness/"
    response = HtmlResponse(url=url, body=mock_html, encoding='utf-8')

    # 3. Instantiate the spider
    spider = PhoneplaceSpider()

    # 4. Call the spider's parse method with our fake response
    # The parse method returns a generator, so we can convert it to a list
    results = list(spider.parse(response))

    # 5. Assert that we got exactly one item back
    assert len(results) == 1

    # 6. Assert that the data extracted data i exactly what we want/expect
    extracted_item = results[0]
    assert extracted_item["product_name"] == "Samsung Galaxy S23 Ultra"
    assert extracted_item["price"] == "185000.0"
    assert extracted_item["source_url"] == "https://www.phoneplacekenya.com/product/samsung-galaxy-s23/"
    assert extracted_item["source_brand"] == "Phoneplace"
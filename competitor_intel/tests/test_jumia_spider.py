import pytest
from scrapy.http import HtmlResponse

# Import the spider (we will name it JumiaSpider)
from competitor_intel.spiders.jumia import JumiaSpider

def test_jumia_spider_extracts_data():
    """Test that the spider correctly parses a mock Jumia product card."""
    mock_html = """
    <html><body>
        <article class="prd">
            <a href="/samsung-galaxy-s24-5g.html" class="core">
                <h3 class="name">Samsung Galaxy S24 5G - 128GB ROM + 8GB RAM</h3>
            </a>
            <div class="prc">
                KSh 149,999
            </div>
        </article>
    </body></html>
    """
    url = "https://www.jumia.co.ke/mobile-phones/"
    response = HtmlResponse(url=url, body=mock_html, encoding='utf-8')
    spider = JumiaSpider()
    
    results = list(spider.parse(response))
    
    assert len(results) == 1
    extracted_item = results[0]
    assert extracted_item["product_name"] == "Samsung Galaxy S24 5G - 128GB ROM + 8GB RAM"
    assert extracted_item["price"] == 149999.0  # FIXED: Expect float, not string
    assert extracted_item["source_url"] == "https://www.jumia.co.ke/samsung-galaxy-s24-5g.html"
    assert extracted_item["source_brand"] == "Jumia Kenya"
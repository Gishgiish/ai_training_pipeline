import pytest
from scrapy.exceptions import DropItem

from competitor_intel.pipelines import PydanticValidationPipeline

def test_valid_item_passes_through_pipeline():
    """Test that a valid dictionary passes validation and is returned"""

    pipeline = PydanticValidationPipeline()

    valid_item = {
        "product_name": "Samsung Galaxy S23 Ultra",
        "price": 150000.00,
        "source_url": "https://phoneplace.co.ke/23",
        "source_brand": "Phoneplace"
    }

    # Scrapy pipeline method process_item will be used here
    result = pipeline.process_item(valid_item, spider=None)

    # Expect a clean library
    assert isinstance(result, dict)
    assert result["price"] == 150000.00

    #Pydantic should auto-add default currency and the timestamp
    assert result["currency"] == "KES"

def test_invalid_item_is_dropped():
    """Test that an invalid dictionary raises Scrapy's DropItem exception."""

    pipeline = PydanticValidationPipeline()

    invalid_item = {
        "product_name": "Fake phone",
        "price": -500.00,
        "source_url": "https://fake.com",
        "source_brand": "FakeBrand"
    }

    # Expect pipeline to catch the error
    with pytest.raises(DropItem):
        pipeline.process_item(invalid_item, spider=None)
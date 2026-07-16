import pytest
from pydantic import ValidationError
from datetime import datetime

from competitor_intel.models import Product

def test_valid_product_creation():
    """Test that a perfectly clean product passes validation."""

    product = Product(
        product_name = "Samsung Galaxy S23 Ultra",
        price = 185000.50,
        currency = "KES",
        availability = "In Stock",
        source_url = "https://www.phoneplacekenya.com/product/samsung-23",
        source_brand = "Phoneplace"
    )

    # Assertions to enure that the model accepted the data correctly
    assert product.product_name == "Samsung Galaxy S23 Ultra"
    assert product.price == 185000.50
    assert product.currency == "KES"
    assert isinstance(product.scraped_at, datetime) 

def test_invalid_price_raises_error():
    """Test that a negative price is rejected by the pydantic bouncer."""

    # Expect error upon negative price
    with pytest.raises(ValidationError):
        Product(
            product_name = "Fake Phone",
            price = -500.00,
            source_url = "https://fake.com",
            source_brand = "Fake Brand"
        )
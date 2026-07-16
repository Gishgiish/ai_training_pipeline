from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

class Product(BaseModel):
    """ Pydantic model defining the strict schema for our craped electronics data.
    This ensures only clean, validated data reaches our AI pipeline. """

    # Show a required field by adding min_length to ensure it is not an empty string
    product_name: str = Field(..., min_length=3, description="The name of the electronic product")

    # Ensure no negative value in price by adding gt=0
    price: float = Field(..., gt=0, description="Price of the product must be greater than zero(0)")

    currency: str = Field(default="KES", description="Currency code")
    availability: Optional[str] = Field(default="Unknown", description="Stock status")

    source_url: str = Field(..., min_length=5, description="URL where the product was scraped")
    source_brand: str = Field(..., min_length=2, description="The retailer's name")

    # default_factory to mean thi function runs automatically every time a new product is created
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp of extraction")
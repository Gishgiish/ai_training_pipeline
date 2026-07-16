import logging
from pydantic import ValidationError
from scrapy.exceptions import DropItem

from competitor_intel.models import Product


logger = logging.getLogger(__name__)


class PydanticValidationPipeline:
    """
    Scrapy Item Pipeline that validates scraped dictionaries against our Pydantic Product model
    """

    def process_item(self, item):
        """
        This method is called for evert Item yielded by the spider.
        """

        try:
            # 1. Attempt to validate the raw dictionary using pydantic
            validate_product = Product(**item)

            # 2. If successful, convert the pydantic model back to dictionary 
            # so Scrapy's default exporters (CSV/JSON) can easily save it. 
            return validate_product.model_dump()

        except ValidationError as e:
            # 3. If pydantic rejects the data, we tell Scrapy to drop it
            raise DropItem(f"Validation failed! Errors: {e}")


class DataQualityMonitorPipeline:
    """
    Monitors the health of the scraping pipeline.
    Tracks total items and dropped items. If the drop rate exceeds 30%,
    it logs a CRITICAL alert for the engineering team. 
    """

    def __init__(self):
        self.total_count = 0
        self.dropped_count = 0
        self.drop_threshold = 0.30 # 30%

    def open_spider(self, spider):
        """ Called when spider starts. """

        self.total_count = 0
        self.dropped_count = 0
        logger.info(f"Data Quality Monitor started for spider: {spider.name} ")

    def process_item(self, item, spider):
        """Called for every item yielded by the spider."""

        self.total_count += 1



        return item

    def item_dropped(self, item, spider, exception):
        """ Called when any item is dropped by ANY pipeline."""

        if isinstance(exception, DropItem):
            self.dropped_count += 1

    def close_spider(self, spider):
        """ Called when spider finishe. Calculates the final health metrics."""

        if self.total_count == 0:
            logger.warning(f"Spider {spider.name} scrapped ZERO items!")
            return
        
        drop_rate = (self.dropped_count / self.total_count) * 100

        logger.info(f"Final stat for {spider.name}: {self.total_count} total, {self.dropped_count} dropped ({drop_rate:.1f}%)")

        if drop_rate > (self.drop_threshold * 100):
            # The alert itself
            logger.critical(
                f"CRITICAL DATA QUALITY ALERT for {spider.name}! "
                f"Drop rate is {drop_rate:.1f}%, which exceeds the {self.drop_threshold * 100}% threshold. "
                f"Immediate investigation required"
            )

    
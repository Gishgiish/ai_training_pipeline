import pytest
import logging
from scrapy.exceptions import DropItem
# FIX 1: Removed the incorrect HttpErrorMixin and unused Request imports
from competitor_intel.pipelines import DataQualityMonitorPipeline

class MockSpider:
    """ A mock spider to satisfy Scrapy's pipeline requirements. """
    name = "mock_spider"

def test_monitoring_pipeline_passes_on_good_data(caplog):
    """Test that good data (0% drop rate) does NOT trigger a critical alert."""
    pipeline = DataQualityMonitorPipeline()
    spider = MockSpider()
    
    # Simulate spider opening
    pipeline.open_spider(spider)
    
    # Process 10 valid items
    for i in range(10):
        pipeline.process_item({"price": 100.0}, spider)
        
    # Simulate spider closing
    with caplog.at_level(logging.CRITICAL):
        pipeline.close_spider(spider)
        
    # Assert that NO critical error was logged
    assert "CRITICAL DATA QUALITY ALERT" not in caplog.text

def test_monitoring_pipeline_alerts_on_high_drop_rate(caplog):
    """Test that a high drop rate (>30%) triggers a CRITICAL alert."""
    pipeline = DataQualityMonitorPipeline()
    spider = MockSpider()
    
    # Simulate spider opening
    pipeline.open_spider(spider)
    
    # Process 10 valid items
    for i in range(10):
        pipeline.process_item({"price": 100.0}, spider)
        
    # FIX 2: Simulate 5 dropped items. 
    # Because a monitoring pipeline usually just *observes* drops from other pipelines 
    # rather than causing them, we manually increment the counter to simulate the 50% drop rate.
    for i in range(5):
        pipeline.dropped_count += 1 
        
    # Simulate spider closing 
    with caplog.at_level(logging.CRITICAL):
        pipeline.close_spider(spider)
        
    # Assert that a critical error WAS logged
    assert "CRITICAL DATA QUALITY ALERT" in caplog.text
    assert "50.0%" in caplog.text
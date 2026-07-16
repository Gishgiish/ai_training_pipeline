import sys
import os
import subprocess
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_spiders():
    print("Initializing Scrapy Engine...")
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    # Addition of spiders
    process.crawl('phoneplace')
    process.crawl('jumia')
    process.crawl('samsung')

    # This blocks until all spiders are finished
    process.start()

def run_ai_report():
    print("\n Starting AI report generation...")
    result = subprocess.run([sys.executable, "generate_report.py"], capture_output=True, text=True)

    if result.returncode == 0:
        print("AI report generated successfully!")
        print(result.stdout)

    else:
        print("Error generating AI report:")
        print(result.stderr)

if __name__ == "__main__":
    print("Starting Competitor Intelligence pipeline....")
    run_spiders()
    run_ai_report()
    print("\n Pipeline execution completed!")
# AI Competitor Intelligence Pipeline

A robust, scalable, and AI-powered web scraping pipeline designed to extract, validate, and analyze competitor pricing data from major Kenyan e-commerce retailers. Built with Scrapy, Pydantic, and Groq AI, this system transforms raw HTML into actionable market intelligence reports.

##  Features
- **Multi-Target Scraping**: Dedicated spiders for Jumia, Phoneplace Kenya, and Samsung/Avechi Kenya.
- **JavaScript Rendering**: Integrated `scrapy-playwright` to bypass lazy-loading and dynamic content barriers.
- **Strict Data Validation**: Pydantic models enforce data integrity before items enter the pipeline.
- **Resilience & Monitoring**: Custom `DataQualityMonitorPipeline` tracks drop rates and triggers critical alerts if data quality falls below a 30% threshold.
- **AI-Powered Analytics**: Aggregates scraped data and uses Groq (Llama 3) to generate professional, markdown-formatted market intelligence reports.
- **Streamlit Dashboard**: (Optional/Planned) Visualizes pricing trends and report outputs.

## Tech Stack
- **Language**: Python 3.12+
- **Scraping**: Scrapy 2.17+, Scrapy-Playwright
- **Validation**: Pydantic 2.x
- **AI/LLM**: Groq API (`llama-3.3-70b-versatile`)
- **Testing**: Pytest
- **Deployment**: Docker, Render.com

## Quick Start (Local Development)

### 1. Prerequisites
- Python 3.12+
- Git
- A free [Groq API Key](https://console.groq.com/keys)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/Gishgiish/ai_training_pipeline.git
cd ai_training_pipeline

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (required for JS rendering)
playwright install chromium
```
### 3. Environment set up
- Create a .env file in the root directory:
```bash
GROQ_API_KEY=your_groq_api_key_here
STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
```

### 4. Running Spiders
- Navigate to the competitor_intel directory and run a spider:
```bash
cd competitor_intel
scrapy crawl jumia -o ../data/jumia_output.jsonl
scrapy crawl phoneplace -o ../data/phoneplace_output.jsonl
scrapy crawl samsung -o ../data/samsung_output.jsonl
```

### 5. Generating the AI Report
- Once data is scraped, generate the market intelligence report:

``` bash
python generate_report.py
```

--Output will be saved to data/market_intelligence_report.md.

## Testing
- This project strictly follows Test-Driven Development (TDD). To run the test suite:
```bash
pytest tests/ -v
```


# Competitor Intel Module

This directory contains the core Scrapy project, data models, pipelines, and AI report generation logic.

## Directory Structure
```text
competitor_intel/
├── spiders/
│   ├── __init__.py
│   ├── jumia.py          # Jumia Kenya spider (Playwright enabled)
│   ├── phoneplace.py     # Phoneplace Kenya spider (Regex fallbacks)
│   └── samsung.py        # Avechi/Samsung Kenya spider (WooCommerce selectors)
├── __init__.py
├── items.py              # (Legacy, replaced by models.py)
├── models.py             # Pydantic V2 data validation schemas
├── pipelines.py          # PydanticValidation & DataQualityMonitor
├── settings.py           # Scrapy configuration (ROBOTSTXT_OBEY, DOWNLOAD_DELAY, etc.)
├── generate_report.py    # Groq-powered market intelligence aggregator
├── dashboard.py          # Streamlit UI for data visualization
├── Dockerfile            # Containerization instructions
└── requirements.txt      # Python dependencies
```

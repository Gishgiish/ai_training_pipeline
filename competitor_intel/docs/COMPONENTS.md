Component Breakdown
-------------------

### 1\. Spiders (`competitor_intel/spiders/`)

Each spider is tailored to the specific DOM structure of its target:

-   `jumia.py`: Targets `article.prd`, handles heavy JS lazy-loading via Playwright.
-   `phoneplace.py`: Targets `div.product-wrapper`, includes regex fallbacks for price extraction.
-   `samsung.py`: Targets Avechi Kenya's WooCommerce structure (`li.product`, `span.woocommerce-Price-amount`).

### 2\. Data Models (`competitor_intel/models.py`)

A single source of truth for data schema using Pydantic V2:

-   Enforces `product_name` (str), `price` (float, > 0), `source_url` (HttpUrl), and `source_brand` (str).
-   Automatically converts and cleans data types upon instantiation.

### 3\. Pipelines (`competitor_intel/pipelines.py`)

-   `PydanticValidationPipeline`: The first line of defense. Attempts to instantiate the `Product` model. Raises `DropItem` on `ValidationError`.
-   `DataQualityMonitorPipeline`: Observes the pipeline health. Tracks `total_count` and `dropped_count`. If `(dropped / total) > 30%`, it triggers a `logging.CRITICAL` alert for engineering intervention.

### 4\. AI Report Generator (`competitor_intel/generate_report.py`)

-   Aggregation: Reads all `.jsonl` files, calculates average prices, and samples top 5 products per store to minimize LLM token usage.
-   Generation: Sends a structured prompt to Groq's `llama-3.3-70b-versatile` model to generate an executive summary, pricing analysis, and strategic recommendations.

### 5\. Resilience & Error Handling
-------------------------------

-   Selector Fallbacks: Spiders use chained CSS selectors (e.g., `h3.classA::text, h2.classB::text`) to survive minor UI updates.
-   Graceful Degradation: If a price is missing, the item is logged and dropped cleanly without crashing the spider.
-   Dockerized Dependencies: System-level Playwright dependencies are baked into the Docker image, ensuring consistent execution across local and production environments.
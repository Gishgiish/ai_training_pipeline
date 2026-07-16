import json
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 1. Configure Groq API
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found! Please set it in your .env file.")

# Initialize the Groq client
client = Groq(api_key=API_KEY)

def load_and_aggregate_data(data_dir="data"):
    """
    Reads all JSONL files in the data directory and aggregates key metrics.
    This prevents us from hitting LLM token limits with raw data.
    """
    stores_data = {}
    
    # Grab all jsonl files in the data folder
    for filename in os.listdir(data_dir):
        if filename.endswith(".jsonl"):
            store_name = filename.replace("_output.jsonl", "").capitalize()
            filepath = os.path.join(data_dir, filename)
            products = []
            total_price = 0
            valid_prices_count = 0
            
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    item = json.loads(line)
                    products.append(item)
                    
                    # Aggregate price data (pydantic ensured this is a clean float)
                    if item.get("price"):
                        total_price += float(item["price"])
                        valid_prices_count += 1
                        
            avg_price = total_price / valid_prices_count if valid_prices_count > 0 else 0
            stores_data[store_name] = {
                "total_items": len(products),
                "average_price_kes": round(avg_price, 2),
                "sample_products": [p.get("product_name", "Unknown") for p in products[:5]] # send top 5 for context
            }
            
    # FIXED: Return is now correctly outside the 'for' loop so it processes ALL stores
    return stores_data

def generate_ai_report(stores_data):
    """
    Sends the aggregated data to the LLM to generate a strategic market report.
    """
    print("Sending aggregated data for analysis...")
    
    # Prompt to generate a Professional, structured output
    prompt = f"""
    You are an expert E-commerce Market analyst in Kenya.
    I have scraped competitor pricing data for electronics from multiple retailers. 
    Here is the aggregated data:
    {json.dumps(stores_data, indent=2)}
    
    Please generate a concise, professional "Competitor Market Intelligence Report" in markdown format.
    Your report must include:
    1. **Executive Summary**: A 2-sentence overview of the market landscape.
    2. **Pricing Analysis**: Compare the average prices. Who is the premium retailer? Who is the budget-friendly option?
    3. **Inventory Observations**: Note any interesting patterns in the sample products provided. 
    4. **Strategic Recommendation**: One actionable advice for a new retailer entering this market based on this data.
    
    Keep the tone professional, analytical, and data-driven.
    """
    
    try:
        # Call the Groq API using Llama 3.3 70B (Incredibly smart, completely free)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert E-commerce Market analyst in Kenya."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile", 
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error generating report: {e}"

if __name__ == "__main__":
    print("Starting AI Report Generation Pipeline...")
    
    # 1. Aggregate the data
    aggregated_data = load_and_aggregate_data("data")
    
    if not aggregated_data:
        print("No JSONL files found in the 'data' directory. Run your spiders first!")
    else:
        print(f"Successfully aggregated data from {len(aggregated_data)} stores.")
        
        # 2. Generate Report
        report_markdown = generate_ai_report(aggregated_data)
        
        # 3. Save the report
        output_file = "data/market_intelligence_report.md"
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(report_markdown)
            
        print(f"Success! Report saved to '{output_file}'")
        print("\n --- PREVIEW OF REPORT ---")
        print(report_markdown[:500] + "...\n------")
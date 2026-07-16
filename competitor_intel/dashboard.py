import streamlit as st
import pandas as pd
import json
import os
import glob
import sys
import subprocess
import threading
import time
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Competitor Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# 🕒 BACKGROUND SCHEDULER (Every 6 Hours)
# ==========================================
def background_refresh_task():
    """
    A daemon thread that sleeps for 6 hours, then triggers the pipeline.
    It runs silently in the background and logs to the container's stdout.
    """
    while True:
        time.sleep(21600)  # 6 hours = 21,600 seconds
        print(f"[{datetime.now()}] 🔄 Background Scheduler: Starting automated data refresh...")
        try:
            # Use sys.executable to ensure we use the correct Python environment (crucial for Docker)
            subprocess.run([sys.executable, "run_pipeline.py"], check=True)
            print(f"[{datetime.now()}] ✅ Background Scheduler: Refresh completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"[{datetime.now()}] ❌ Background Scheduler: Refresh failed. Error: {e}")

# Start the background thread EXACTLY ONCE per Streamlit session
if "scheduler_started" not in st.session_state:
    st.session_state.scheduler_started = True
    # daemon=True ensures the thread dies automatically if the main Streamlit app stops
    bg_thread = threading.Thread(target=background_refresh_task, daemon=True)
    bg_thread.start()

# ==========================================
# 🖥️ FRONTEND UI
# ==========================================

# --- HEADER ---
st.title("📊 Nairobi E-Commerce Competitor Intelligence")
st.markdown("Real-time market data aggregated from multiple retailers and analyzed by AI.")

# --- SIDEBAR: PIPELINE STATUS & CONTROLS ---
st.sidebar.header("Pipeline Status & Controls")
data_dir = "data"

# Check when the data was last updated
jsonl_files = glob.glob(os.path.join(data_dir, "*.jsonl"))
if jsonl_files:
    latest_file_time = max(os.path.getmtime(f) for f in jsonl_files)
    last_updated = datetime.fromtimestamp(latest_file_time).strftime("%Y-%m-%d %H:%M:%S")
    st.sidebar.success(f"✅ Last Updated: {last_updated}")
else:
    st.sidebar.warning("⚠️ No data found. Run the pipeline first!")

# --- MANUAL REFRESH TRIGGER ---
st.sidebar.markdown("---")
st.sidebar.subheader("Manual Data Refresh")
st.sidebar.caption("Click to fetch the latest prices from all retailers. (Takes ~1-2 mins)")

if st.sidebar.button("🔄 Refresh Data Now", use_container_width=True, type="primary"):
    with st.spinner("🚀 Fetching fresh data... The dashboard will reload automatically."):
        try:
            # Run the pipeline synchronously so we can catch errors and show a spinner
            result = subprocess.run(
                [sys.executable, "run_pipeline.py"],
                capture_output=True,
                text=True
            )
           
            if result.returncode == 0:
                st.sidebar.success("✅ Data refreshed successfully!")
                st.cache_data.clear() # Clear Streamlit's internal cache
                st.rerun()            # Force the UI to reload with new data
            else:
                st.sidebar.error("❌ Pipeline failed. Check container logs for details.")
                print(result.stderr)  # Print error to container logs for debugging
               
        except Exception as e:
            st.sidebar.error(f"❌ Execution Error: {e}")

# --- TABS FOR ORGANIZATION ---
tab1, tab2 = st.tabs(["📦 Scraped Data", "🧠 AI Market Report"])

# --- TAB 1: SCRAPED DATA ---
with tab1:
    st.header("Live Product Listings")
   
    if jsonl_files:
        all_data = []
       
        # Read all JSONL files and combine them
        for file in jsonl_files:
            store_name = os.path.basename(file).replace("_output.jsonl", "").capitalize()
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    item = json.loads(line)
                    item['Store'] = store_name
                    all_data.append(item)
       
        # Convert to Pandas DataFrame
        df = pd.DataFrame(all_data)
       
        # Data Cleaning for Display
        if 'price' in df.columns:
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            df = df.sort_values(by='price', ascending=True)
            df['price_formatted'] = df['price'].apply(lambda x: f"KSh {x:,.2f}" if pd.notnull(x) else "N/A")
        else:
            df['price_formatted'] = "N/A"

        # Sidebar Filters
        st.sidebar.markdown("---")
        st.sidebar.subheader("Filters")
        selected_stores = st.sidebar.multiselect(
            "Select Stores:",
            options=df['Store'].unique(),
            default=df['Store'].unique()
        )
       
        max_price_val = int(df['price'].max()) if not df['price'].empty and pd.notnull(df['price'].max()) else 100000
        min_price, max_price = st.sidebar.slider(
            "Price Range (KSh):",
            0, max_price_val, (0, max_price_val)
        )

        # Apply Filters
        filtered_df = df[df['Store'].isin(selected_stores)]
        filtered_df = filtered_df[(filtered_df['price'] >= min_price) & (filtered_df['price'] <= max_price)]

        # Display Interactive Table
        st.dataframe(
            filtered_df[['Store', 'product_name', 'price_formatted', 'source_url']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Store": st.column_config.TextColumn("Retailer"),
                "product_name": st.column_config.TextColumn("Product Name", width="medium"),
                "price_formatted": st.column_config.TextColumn("Price"),
                "source_url": st.column_config.LinkColumn("Link", display_text="View Product")
            }
        )
       
        st.markdown(f"*Showing {len(filtered_df)} of {len(df)} total products.*")
    else:
        st.info("No data available. Please click 'Refresh Data Now' in the sidebar.")

# --- TAB 2: AI MARKET REPORT ---
with tab2:
    st.header("Strategic Market Analysis")
   
    report_path = os.path.join(data_dir, "market_intelligence_report.md")
   
    if os.path.exists(report_path):
        with open(report_path, 'r', encoding='utf-8') as f:
            report_content = f.read()
       
        st.markdown(report_content)
       
        st.download_button(
            label="📥 Download Full Report (.md)",
            data=report_content,
            file_name="market_intelligence_report.md",
            mime="text/markdown"
        )
    else:
        st.warning("AI Report not found. Ensure the pipeline has completed successfully.")
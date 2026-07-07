# 📊 Product KPI & Sentiment Dashboard

An interactive dashboard built with Python and Streamlit to analyze sales trends alongside real-time customer review sentiment analysis. 

## Features
* **Sales Trends:** Visualizes revenue over time using Plotly.
* **Sentiment Analysis:** Automatically scores customer reviews using TextBlob.
* **Interactive Filtering:** Filter metrics and charts by product category.

## How to Run Locally
1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Download text processing corpora: `python -m textblob.download_corpora`
5. Run the app: `streamlit run app.py`
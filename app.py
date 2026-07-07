import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob

# Page Configuration
st.set_page_config(page_title="Product KPI & Sentiment Dashboard", layout="wide")
st.title("📊 Product KPI & Sentiment Dashboard")
st.markdown("Analyze sales trends alongside real-time customer review sentiment analysis.")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("sample_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    
    # TextBlob Sentiment Processing
    def get_sentiment(text):
        analysis = TextBlob(str(text))
        return analysis.sentiment.polarity
        
    df['Sentiment_Score'] = df['Review'].apply(get_sentiment)
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Missing 'sample_data.csv'. Please make sure the data file exists in the directory.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filter Options")
product_list = ["All"] + list(df['Product'].unique())
selected_product = st.sidebar.selectbox("Select Product Category", product_list)

# Filter Data logic
if selected_product != "All":
    filtered_df = df[df['Product'] == selected_product]
else:
    filtered_df = df

# Metric Computations
total_sales = filtered_df['Sales'].sum()
avg_rating = filtered_df['Rating'].mean()
avg_sentiment = filtered_df['Sentiment_Score'].mean()

# Sentiment Labeling
if avg_sentiment > 0.1:
    sentiment_label = "Positive 😊"
elif avg_sentiment < -0.1:
    sentiment_label = "Negative 😞"
else:
    sentiment_label = "Neutral 😐"

# Top Row KPI Metrics
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(label="💰 Total Revenue ($)", value=f"{total_sales:,}")
with kpi2:
    st.metric(label="⭐ Average Star Rating", value=f"{avg_rating:.2f} / 5.0")
with kpi3:
    st.metric(label="🎭 Overall Sentiment Score", value=f"{avg_sentiment:.2f}", delta=sentiment_label)

st.markdown("---")

# Visualizations Row
chart1, chart2 = st.columns(2)

with chart1:
    st.subheader("Sales Trends Over Time")
    trend_df = filtered_df.groupby('Date')['Sales'].sum().reset_index()
    fig_sales = px.line(trend_df, x='Date', y='Sales', markers=True, 
                        labels={'Sales': 'Revenue ($)', 'Date': 'Timeline'})
    st.plotly_chart(fig_sales, use_container_width=True)

with chart2:
    st.subheader("Review Sentiment vs Product Rating")
    fig_scatter = px.scatter(filtered_df, x='Sentiment_Score', y='Rating', 
                             color='Product', size='Sales', hover_data=['Review'],
                             labels={'Sentiment_Score': 'Sentiment Polarity (-1 to 1)', 'Rating': 'Star Rating'})
    st.plotly_chart(fig_scatter, use_container_width=True)

# Data Details Section
st.subheader("📝 Raw Customer Feedback Records")
st.dataframe(filtered_df[['Date', 'Product', 'Review', 'Rating', 'Sentiment_Score']], use_container_width=True)

# dashboard.py

import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="E-commerce ETL Dashboard", layout="wide")

st.title("📦 E-commerce ETL Dashboard")

# Load cleaned data
csv_path = os.path.join("Data", "cleaned_orders.csv")
if not os.path.exists(csv_path):
    st.error("❌ Cleaned data not found. Please run ETL first.")
    st.stop()

df = pd.read_csv(csv_path)

# Sidebar Filters
st.sidebar.header("🔎 Filters")
if 'category' in df.columns:
    categories = st.sidebar.multiselect("Select Categories", df['category'].unique(), default=df['category'].unique())
    df = df[df['category'].isin(categories)]

if 'order_date' in df.columns:
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    min_date, max_date = df['order_date'].min(), df['order_date'].max()
    date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])
    if len(date_range) == 2:
        df = df[(df['order_date'] >= pd.to_datetime(date_range[0])) & (df['order_date'] <= pd.to_datetime(date_range[1]))]

# Metrics
total_orders = len(df)
total_revenue = df['order_amount'].sum() if 'order_amount' in df.columns else 0
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("🛒 Total Orders", f"{total_orders:,}")
col2.metric("💰 Total Revenue", f"₹ {total_revenue:,.2f}")
col3.metric("📦 Avg Order Value", f"₹ {avg_order_value:,.2f}")

# Visualizations
st.subheader("📊 Orders by Category")
if 'category' in df.columns:
    fig = px.bar(df['category'].value_counts().reset_index(), x='index', y='category', labels={'index': 'Category', 'category': 'Orders'})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("📈 Revenue Over Time")
if 'order_date' in df.columns and 'order_amount' in df.columns:
    revenue_over_time = df.groupby('order_date')['order_amount'].sum().reset_index()
    fig2 = px.line(revenue_over_time, x='order_date', y='order_amount', labels={'order_date': 'Date', 'order_amount': 'Revenue'})
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("🥧 Category Distribution")
if 'category' in df.columns:
    fig3 = px.pie(df, names='category', title='Category Share')
    st.plotly_chart(fig3, use_container_width=True)

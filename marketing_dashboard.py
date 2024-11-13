# -*- coding: utf-8 -*-
"""marketing_dashboard.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/197ePsUvp_miI3HuHdNkuQXU5UYV2lv_p
"""
import openpyxl
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_excel('dataset.xlsx')

# Streamlit header and subheader
st.title("📊 Marketing Campaign Analysis Dashboard")
st.subheader("Analyze and visualize marketing campaign performance")

# Campaign Metrics Calculation
data['Conversions'] = pd.to_numeric(data['Conversions'], errors='coerce')
data['Clicks'] = pd.to_numeric(data['Clicks'], errors='coerce')
data['Total_Spend'] = pd.to_numeric(data['Total_Spend'], errors='coerce')
data['Revenue_Generated'] = pd.to_numeric(data['Revenue_Generated'], errors='coerce')

data['Conversion_Rate'] = (data['Conversions'] / data['Clicks']) * 100
data['CPC'] = data['Total_Spend'] / data['Clicks']
data['CPA'] = data['Total_Spend'] / data['Conversions']
data['ROAS'] = data['Revenue_Generated'] / data['Total_Spend']

# KPI Summary
st.header("🔑 Key Performance Indicators (KPIs)")
kpis = {
    'Total Impressions': data['Impressions'].sum(),
    'Total Clicks': data['Clicks'].sum(),
    'Total Conversions': data['Conversions'].sum(),
    'Total Spend': data['Total_Spend'].sum(),
    'Total Revenue': data['Revenue_Generated'].sum(),
    'Average CTR': (data['Clicks'].sum() / data['Impressions'].sum()) * 100,
    'Overall ROAS': data['Revenue_Generated'].sum() / data['Total_Spend'].sum()
}
st.write(kpis)

# Ensure numeric columns for aggregation
numeric_columns = ['Conversion_Rate', 'CPC', 'CPA', 'ROAS', 'Total_Spend', 'Revenue_Generated']
data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Layout: Use columns for better organization
col1, col2 = st.columns(2)

with col1:
    # Visualization of Channel Comparison
    st.subheader("📊 Conversion Rate by Marketing Channel")
    channel_metrics = data.groupby('Marketing_Channel')[numeric_columns].mean().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=channel_metrics, x='Marketing_Channel', y='Conversion_Rate', ax=ax)
    st.pyplot(fig)

    # CTR by Marketing Channel
    st.subheader("📈 Click-Through Rate (CTR) by Marketing Channel")
    channel_metrics['CTR'] = (channel_metrics['Clicks'] / channel_metrics['Impressions']) * 100
    fig, ax = plt.subplots()
    sns.barplot(data=channel_metrics, x='Marketing_Channel', y='CTR', ax=ax)
    st.pyplot(fig)

with col2:
    # Spend Distribution Pie Chart
    st.subheader("💰 Spend Distribution by Marketing Channel")
    fig, ax = plt.subplots()
    ax.pie(channel_metrics['Total_Spend'], labels=channel_metrics['Marketing_Channel'], autopct='%1.1f%%')
    st.pyplot(fig)

    # Revenue vs Spend
    st.subheader("💵 Revenue vs Total Spend by Campaign")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=data, x='Total_Spend', y='Revenue_Generated', hue='Marketing_Channel', ax=ax)
    ax.set_title("Revenue vs Total Spend")
    st.pyplot(fig)

# Monthly Trends Layout
st.header("📅 Monthly Trends in Campaign Performance")
data['End_Date'] = pd.to_datetime(data['End_Date'], errors='coerce')
data['Month_Year'] = data['End_Date'].dt.to_period("M").astype(str)

time_metrics = data.groupby('Month_Year').agg({
    'Impressions': 'sum',
    'Clicks': 'sum',
    'Conversions': 'sum',
    'Total_Spend': 'sum',
    'Revenue_Generated': 'sum'
}).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=time_metrics, x='Month_Year', y='Impressions', label='Impressions', marker='o')
sns.lineplot(data=time_metrics, x='Month_Year', y='Clicks', label='Clicks', marker='o')
sns.lineplot(data=time_metrics, x='Month_Year', y='Conversions', label='Conversions', marker='o')
st.pyplot(fig)

# Add more visualizations using expander
with st.expander("See Additional Analysis"):
    # 3. CPA Distribution
    st.subheader("📉 Cost per Acquisition (CPA) Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=data, x='Marketing_Channel', y='CPA', ax=ax)
    ax.set_title("CPA Distribution by Marketing Channel")
    st.pyplot(fig)

    # 4. ROAS Heatmap
    st.subheader("🌡️ ROAS Heatmap")
    channel_monthly_roas = data.groupby(['Month_Year', 'Marketing_Channel']).agg({'ROAS': 'mean'}).reset_index()
    heatmap_data = channel_monthly_roas.pivot('Month_Year', 'Marketing_Channel', 'ROAS')
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(heatmap_data, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("ROAS Heatmap by Marketing Channel and Month")
    st.pyplot(fig)

    # 5. Campaign Performance Over Time (Stacked Area Chart)
    st.subheader("📊 Campaign Performance Over Time")
    time_metrics.set_index('Month_Year', inplace=True)
    fig, ax = plt.subplots(figsize=(12, 6))
    time_metrics[['Conversions', 'Clicks', 'Revenue_Generated']].plot.area(stacked=True, ax=ax)
    ax.set_title("Campaign Performance (Conversions, Clicks, Revenue) Over Time")
    st.pyplot(fig)

    # 6. Impressions Distribution
    st.subheader("📉 Impressions Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['Impressions'], kde=True, bins=20, ax=ax)
    ax.set_title("Distribution of Impressions")
    st.pyplot(fig)

# Footer section with credits and info
st.markdown("""
---
Created with ❤️ by Hamza Amr
""")


# -*- coding: utf-8 -*-
import openpyxl
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_excel('dataset.xlsx')

# Streamlit header
st.title("Marketing Campaign Analysis Dashboard")

# Campaign Metrics Calculation
# Ensure numeric columns for calculations
data['Conversions'] = pd.to_numeric(data['Conversions'], errors='coerce')
data['Clicks'] = pd.to_numeric(data['Clicks'], errors='coerce')
data['Total_Spend'] = pd.to_numeric(data['Total_Spend'], errors='coerce')
data['Revenue_Generated'] = pd.to_numeric(data['Revenue_Generated'], errors='coerce')

# Calculate metrics
data['Conversion_Rate'] = (data['Conversions'] / data['Clicks']) * 100
data['CPC'] = data['Total_Spend'] / data['Clicks']
data['CPA'] = data['Total_Spend'] / data['Conversions']
data['ROAS'] = data['Revenue_Generated'] / data['Total_Spend']

# KPI Summary
st.header("Key Performance Indicators (KPIs)")
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

# Group by 'Marketing_Channel' and aggregate the necessary metrics
channel_metrics = data.groupby('Marketing_Channel')[numeric_columns].mean().reset_index()

# Ensure there are no NaN or invalid values in 'Clicks' and 'Impressions'
channel_metrics['Clicks'] = pd.to_numeric(channel_metrics['Clicks'], errors='coerce')
channel_metrics['Impressions'] = pd.to_numeric(channel_metrics['Impressions'], errors='coerce')

# Calculate CTR (Click-Through Rate) by Marketing Channel
channel_metrics['CTR'] = (channel_metrics['Clicks'] / channel_metrics['Impressions']) * 100

# Create tabs for different plots using st.selectbox or st.radio
tab = st.selectbox("Select a Plot", ("Overview", "Conversion Rate & CTR", "Monthly Trends", "Spend Distribution", "Revenue Distribution", "CPA Distribution", "ROAS Distribution"))

if tab == "Overview":
    st.header("Key Performance Indicators (KPIs)")
    st.write(kpis)

elif tab == "Conversion Rate & CTR":
    st.header("Conversion Rate and CTR by Marketing Channel")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=channel_metrics, x='Marketing_Channel', y='Conversion_Rate', color='b', label='Conversion Rate', ax=ax)
    sns.barplot(data=channel_metrics, x='Marketing_Channel', y='CTR', color='g', label='Click-Through Rate', ax=ax)
    plt.title("Comparison of Conversion Rate and CTR by Channel")
    ax.set_ylabel("Percentage (%)")
    ax.legend()
    st.pyplot(fig)

elif tab == "Monthly Trends":
    st.header("Monthly Trends in Campaign Performance")
    data['End_Date'] = pd.to_datetime(data['End_Date'], errors='coerce')  # Ensure date column is datetime
    data['Month_Year'] = data['End_Date'].dt.to_period("M").astype(str)  # Extract year-month period
    time_metrics = data.groupby('Month_Year').agg({
        'Impressions': 'sum',
        'Clicks': 'sum',
        'Conversions': 'sum',
        'Total_Spend': 'sum',
        'Revenue_Generated': 'sum'
    }).reset_index()

    # Plotting the trends
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=time_metrics, x='Month_Year', y='Impressions', label='Impressions', marker='o')
    sns.lineplot(data=time_metrics, x='Month_Year', y='Clicks', label='Clicks', marker='o')
    sns.lineplot(data=time_metrics, x='Month_Year', y='Conversions', label='Conversions', marker='o')
    sns.lineplot(data=time_metrics, x='Month_Year', y='Revenue_Generated', label='Revenue Generated', marker='o', linestyle='--')
    st.pyplot(fig)

elif tab == "Spend Distribution":
    st.header("Spend Distribution by Marketing Channel")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(channel_metrics['Total_Spend'], labels=channel_metrics['Marketing_Channel'], autopct='%1.1f%%')
    plt.title("Spend Distribution by Channel")
    st.pyplot(fig)

elif tab == "Revenue Distribution":
    st.header("Revenue Distribution by Marketing Channel")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=channel_metrics, x='Marketing_Channel', y='Revenue_Generated', ax=ax)
    plt.title("Revenue by Marketing Channel")
    ax.set_ylabel("Revenue Generated")
    st.pyplot(fig)

elif tab == "CPA Distribution":
    st.header("Cost per Acquisition (CPA) by Marketing Channel")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=channel_metrics, x='Marketing_Channel', y='CPA', ax=ax)
    plt.title("Cost per Acquisition (CPA) by Marketing Channel")
    ax.set_ylabel("Cost per Acquisition")
    st.pyplot(fig)

elif tab == "ROAS Distribution":
    st.header("Return on Ad Spend (ROAS) by Marketing Channel")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=channel_metrics, x='Marketing_Channel', y='ROAS', ax=ax)
    plt.title("Return on Ad Spend (ROAS) by Marketing Channel")
    ax.set_ylabel("ROAS")
    st.pyplot(fig)

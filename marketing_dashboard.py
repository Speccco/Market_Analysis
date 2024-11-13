import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_excel('dataset.xlsx')

# Streamlit header
st.title("Marketing Campaign Analysis Dashboard")

# Set style for seaborn
sns.set(style="whitegrid", palette="muted", font_scale=1.2)

# Campaign Metrics Calculation
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

# Layout for KPIs using columns
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Total Impressions")
    st.markdown(f"<h3 style='text-align: center; color: #2a9d8f'>{data['Impressions'].sum():,}</h3>", unsafe_allow_html=True)

with col2:
    st.subheader("Total Clicks")
    st.markdown(f"<h3 style='text-align: center; color: #2a9d8f'>{data['Clicks'].sum():,}</h3>", unsafe_allow_html=True)

with col3:
    st.subheader("Total Conversions")
    st.markdown(f"<h3 style='text-align: center; color: #2a9d8f'>{data['Conversions'].sum():,}</h3>", unsafe_allow_html=True)

# Next row of KPIs
col4, col5, col6 = st.columns(3)

with col4:
    st.subheader("Total Spend")
    st.markdown(f"<h3 style='text-align: center; color: #264653'>${data['Total_Spend'].sum():,.2f}</h3>", unsafe_allow_html=True)

with col5:
    st.subheader("Total Revenue")
    st.markdown(f"<h3 style='text-align: center; color: #264653'>${data['Revenue_Generated'].sum():,.2f}</h3>", unsafe_allow_html=True)

with col6:
    st.subheader("Average CTR (%)")
    avg_ctr = (data['Clicks'].sum() / data['Impressions'].sum()) * 100
    st.markdown(f"<h3 style='text-align: center; color: #264653'>{avg_ctr:,.2f}%</h3>", unsafe_allow_html=True)

# Final row of KPIs
col7, col8 = st.columns(2)

with col7:
    st.subheader("Overall ROAS")
    roas = data['Revenue_Generated'].sum() / data['Total_Spend'].sum()
    st.markdown(f"<h3 style='text-align: center; color: #e9c46a'>{roas:,.2f}</h3>", unsafe_allow_html=True)

with col8:
    st.subheader("Average CPC")
    avg_cpc = data['Total_Spend'].sum() / data['Clicks'].sum()
    st.markdown(f"<h3 style='text-align: center; color: #e9c46a'>${avg_cpc:,.2f}</h3>", unsafe_allow_html=True)

# Tabs for different plots
tabs = st.selectbox("Select a Plot", ['Conversion Rate by Marketing Channel', 'CPC vs Conversion Rate', 'ROAS by Channel', 'Spend Trend Over Time'])

# Plot for Conversion Rate by Marketing Channel
if tabs == 'Conversion Rate by Marketing Channel':
    st.subheader("Conversion Rate by Marketing Channel")
    channel_metrics = data.groupby('Marketing_Channel')[['Conversion_Rate', 'Clicks', 'Impressions']].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=channel_metrics, x='Marketing_Channel', y='Conversion_Rate', ax=ax, palette="Blues_d")
    ax.set_title("Conversion Rate by Marketing Channel", fontsize=16)
    ax.set_xlabel('Marketing Channel', fontsize=12)
    ax.set_ylabel('Conversion Rate (%)', fontsize=12)
    fig.tight_layout()
    st.pyplot(fig)

# Plot for CPC vs Conversion Rate
elif tabs == 'CPC vs Conversion Rate':
    st.subheader("CPC vs Conversion Rate")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=data, x='CPC', y='Conversion_Rate', hue='Marketing_Channel', palette='Set2', edgecolor='black', s=100, alpha=0.7)
    ax.set_title("CPC vs Conversion Rate", fontsize=16)
    ax.set_xlabel('Cost per Click (CPC)', fontsize=12)
    ax.set_ylabel('Conversion Rate (%)', fontsize=12)
    fig.tight_layout()
    st.pyplot(fig)

# Plot for ROAS by Marketing Channel
elif tabs == 'ROAS by Channel':
    st.subheader("ROAS by Marketing Channel")
    channel_metrics = data.groupby('Marketing_Channel')[['ROAS', 'Total_Spend']].mean().reset_index()  # Corrected calculation
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=channel_metrics, x='Marketing_Channel', y='ROAS', ax=ax, palette='viridis')
    ax.set_title("ROAS by Marketing Channel", fontsize=16)
    ax.set_xlabel('Marketing Channel', fontsize=12)
    ax.set_ylabel('ROAS', fontsize=12)
    fig.tight_layout()
    st.pyplot(fig)

# Plot for Spend Trend Over Time
elif tabs == 'Spend Trend Over Time':
    st.subheader("Spend Trend Over Time")
    data['End_Date'] = pd.to_datetime(data['End_Date'], errors='coerce')  # Ensure date column is datetime
    data['Month_Year'] = data['End_Date'].dt.to_period("M").astype(str)
    spend_trends = data.groupby('Month_Year')['Total_Spend'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=spend_trends, x='Month_Year', y='Total_Spend', marker='o', color='coral', linewidth=3)
    ax.set_title("Marketing Spend Over Time", fontsize=16)
    ax.set_xlabel('Month/Year', fontsize=12)
    ax.set_ylabel('Total Spend ($)', fontsize=12)
    fig.tight_layout()
    st.pyplot(fig)

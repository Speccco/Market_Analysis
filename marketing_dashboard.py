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

# Create layout for KPIs using columns
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

# Make sure the rest of your code follows, e.g. visualizations and more

# Channel Metrics Visualization Example
channel_metrics = data.groupby('Marketing_Channel')[['Conversion_Rate', 'Clicks', 'Impressions']].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=channel_metrics, x='Marketing_Channel', y='Conversion_Rate', ax=ax)
ax.set_title("Conversion Rate by Marketing Channel")
st.pyplot(fig)

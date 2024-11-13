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

# Create Tabs
tabs = ['Overview', 'Channel Comparison', 'Trends', 'Spend Distribution', 'CTR and CPC', 'Correlations']
selected_tab = st.selectbox("Select Tab", tabs)

if selected_tab == 'Overview':
    st.header("Overview of Marketing Metrics")
    st.write(kpis)

elif selected_tab == 'Channel Comparison':
    st.header("Conversion Rate by Marketing Channel")
    channel_metrics = data.groupby('Marketing_Channel')[numeric_columns].mean().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(data=channel_metrics, x='Marketing_Channel', y='Conversion_Rate', ax=ax)
    st.pyplot(fig)

elif selected_tab == 'Trends':
    st.header("Monthly Trends in Campaign Performance")
    data['End_Date'] = pd.to_datetime(data['End_Date'], errors='coerce')  # Ensure date column is datetime
    data['Month_Year'] = data['End_Date'].dt.to_period("M").astype(str)
    time_metrics = data.groupby('Month_Year').sum().reset_index()

    fig, ax = plt.subplots()
    sns.lineplot(data=time_metrics, x='Month_Year', y='Impressions', label='Impressions', marker='o')
    sns.lineplot(data=time_metrics, x='Month_Year', y='Clicks', label='Clicks', marker='o')
    sns.lineplot(data=time_metrics, x='Month_Year', y='Conversions', label='Conversions', marker='o')
    st.pyplot(fig)

elif selected_tab == 'Spend Distribution':
    st.header("Spend Distribution by Marketing Channel")
    channel_metrics = data.groupby('Marketing_Channel')[['Total_Spend']].sum().reset_index()

    fig, ax = plt.subplots()
    ax.pie(channel_metrics['Total_Spend'], labels=channel_metrics['Marketing_Channel'], autopct='%1.1f%%')
    st.pyplot(fig)

elif selected_tab == 'CTR and CPC':
    st.header("Click-Through Rate (CTR) and Cost per Click (CPC) by Marketing Channel")
    # Calculate CTR
    channel_metrics = data.groupby('Marketing_Channel')[['Clicks', 'Impressions', 'CPC']].sum().reset_index()
    channel_metrics['CTR'] = (channel_metrics['Clicks'] / channel_metrics['Impressions']) * 100

    fig, ax = plt.subplots(1, 2, figsize=(14, 6))

    # CTR Plot
    sns.barplot(data=channel_metrics, x='Marketing_Channel', y='CTR', ax=ax[0])
    ax[0].set_title('CTR by Channel')

    # CPC Plot
    sns.barplot(data=channel_metrics, x='Marketing_Channel', y='CPC', ax=ax[1])
    ax[1].set_title('CPC by Channel')

    st.pyplot(fig)

elif selected_tab == 'Correlations':
    st.header("Correlations Between Metrics")
    correlation_matrix = data[numeric_columns].corr()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

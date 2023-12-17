import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(
    page_title="NHTSA Recalls",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align: center; font-size: 5em;'>NHTSA Recalls Dashboard</h1>",
    unsafe_allow_html=True
)


# Custom CSS to reduce the gap between columns in col1
st.markdown(
    """
    <style>
        .css-1aumxhk {
            margin-right: 0px !important;
            padding-right: 0px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def get_data():
    df = pd.read_csv('Recalls_Data.csv')
    df = df.drop(['NHTSA ID', 'Recall Link', 'Subject', 'Mfr Campaign Number', 'Recall Description',
                  'Do Not Drive Advisory', 'Park Outside Advisory ', 'Consequence Summary',
                  'Corrective Action', 'Completion Rate % (Blank - Not Reported)'], axis=1)
    df['Report Received Date'] = pd.to_datetime(df['Report Received Date'], format='%m/%d/%Y')
    df['Year'] = df['Report Received Date'].dt.year
    return df

@st.cache_data
def calculate_metrics(df):
    affected_count = round(df['Potentially Affected'].sum() / 1_000_000, 2)
    avg_per_recall = round(df['Potentially Affected'].mean(), 2)

    avg_recall_per_year = df.groupby('Year')['Potentially Affected'].mean().reset_index()
    total_potentially_affected_per_year = df.groupby('Year')['Potentially Affected'].sum().reset_index()
    recalls_per_year = df.groupby('Year').size().reset_index(name='Number of Recalls')
    recalls_by_manufacturer = df['Manufacturer'].value_counts().reset_index(name='Number of Recalls')
    recalls_by_manufacturer = recalls_by_manufacturer.head(20).sort_values(by='Number of Recalls', ascending=False)

    return affected_count, avg_per_recall, avg_recall_per_year, total_potentially_affected_per_year, recalls_per_year, recalls_by_manufacturer

df = get_data()
(affected_count, avg_per_recall, avg_recall_per_year,
 total_potentially_affected_per_year, recalls_per_year, recalls_by_manufacturer) = calculate_metrics(df)

col1, col2 = st.columns([0.5, 0.5])  # Adjust the width of col1

with col1:
    m1, m2, m3 = st.columns(3)
    m1.metric(label='RECALLS', value=len(df))
    m2.metric(label='POTENTIALLY AFFECTED', value=f'{affected_count:.2f} M')
    m3.metric(label='AVG. UNITS PER RECALL', value=f'{avg_per_recall:.2f}')
    style_metric_cards()


    fig_avg_recall = px.bar(avg_recall_per_year, x='Year', y='Potentially Affected', title='Average Recall per Year',
                            labels={'Potentially Affected': 'Average Potentially Affected'},
                            template='plotly_dark')
    fig_avg_recall.update_traces(marker_color='#9AD8E1')
    st.plotly_chart(fig_avg_recall, use_container_width=True, height=200,style="background-color: #9AD8E1")  # Increase the height of col1

    fig_potentially_affected = px.bar(total_potentially_affected_per_year,
                                      x='Year', y='Potentially Affected',
                                      title='Potentially Affected per Year',
                                      labels={'Potentially Affected': 'Potentially Affected'},
                                      template='plotly_dark')
    
    fig_potentially_affected.update_traces(marker_color='#9AD8E1')
    
    st.plotly_chart(fig_potentially_affected, use_container_width=True, height=200)  # Increase the height of col1

    
    fig_recalls_per_year = px.bar(recalls_per_year, x='Year', y='Number of Recalls',
                                  title='Number of Recalls per Year',
                                  labels={'Number of Recalls': 'Number of Recalls'},
                                  template='plotly_dark')
    fig_recalls_per_year.update_traces(marker_color='#9AD8E1')
    st.plotly_chart(fig_recalls_per_year, use_container_width=True, height=200)  # Increase the height of col1



with col2:
    option = st.selectbox("Choose a Measure", ["Recalls", "Potentially Affected"])

    if option == "Recalls":
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")

        recalls_by_manufacturer = recalls_by_manufacturer.sort_values(by='Number of Recalls', ascending=True)

        fig, ax = plt.subplots(figsize=(8, 20))
        bars = ax.barh(recalls_by_manufacturer['Manufacturer'], recalls_by_manufacturer['Number of Recalls'], color='#9AD8E1')

        for bar in bars:
            plt.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, f'{bar.get_width():,.0f}', ha='left', va='center')

        plt.title('Top 20 Recalls by Manufacturer')
        plt.xlabel('Number of Recalls')
        plt.ylabel('Manufacturer')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        st.pyplot(fig, use_container_width=True)

    elif option == "Potentially Affected":
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")

        #st.subheader("Top 20 Potentially Affected by Manufacturer")
    
        # Group Potentially Affected by Manufacturer
        potentially_affected_by_manufacturer = df.groupby('Manufacturer')['Potentially Affected'].sum().reset_index()
        potentially_affected_by_manufacturer = potentially_affected_by_manufacturer.sort_values(by='Potentially Affected', ascending=True).tail(20)

        # Convert numbers to million and add 'M'
        potentially_affected_by_manufacturer['Potentially Affected (M)'] = potentially_affected_by_manufacturer['Potentially Affected'] / 1e6
        labels = potentially_affected_by_manufacturer['Manufacturer']
        values = potentially_affected_by_manufacturer['Potentially Affected (M)']

        fig, ax = plt.subplots(figsize=(8, 20))
        bars = ax.barh(labels, values, color='#9AD8E1')

        for bar in bars:
            plt.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2, f'{bar.get_width():,.2f} M', ha='left', va='center')

        plt.title('Top 20 Potentially Affected by Manufacturer')
        plt.xlabel('Potentially Affected (Million)')
        plt.ylabel('Manufacturer')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        st.pyplot(fig, use_container_width=True)
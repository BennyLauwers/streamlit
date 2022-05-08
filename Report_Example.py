import streamlit as st
import numpy as np
import pandas as pd
import datetime
from datetime import datetime as dt

st.set_page_config(layout="wide")
st.header("Viu More Safety Detection")
col10, col11 = st.sidebar.columns([2, 1])
col10.image("logo.png")
col11.header("   ")
select_box = st.sidebar.selectbox("Navigation Menu", ("Live Stream", "Report"))


today = datetime.date.today()
now = dt.now().strftime("%H:%M:%S")

if select_box == "Live Stream":
    today_formatted = today.strftime('%d %b %Y')
    st.subheader(str(today_formatted) + " - " + str(now))
    col1, col2, col3 = st.columns([4, 1, 2])
    video_file = open('final.mp4', 'rb')
    video_bytes = video_file.read()

    df = pd.read_csv('Report.csv', delimiter=';')
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df = df.sort_values(by = 'Date')
    todays_alerts = (df['Date'] == str(today))
    todays_alerts_dataframe = df.loc[todays_alerts]
    todays_alert_values = todays_alerts_dataframe['Alerts'].values
    print(todays_alert_values)
    
    yesterday = today - datetime.timedelta(days=1)
    yesterdays_alerts = (df['Date'] == str(yesterday))
    yesterdays_alerts_dataframe = df.loc[yesterdays_alerts]
    yesterdays_alert_values = yesterdays_alerts_dataframe['Alerts'].values
    print(yesterdays_alert_values)

    delta = todays_alert_values - yesterdays_alert_values


    col1.video(video_bytes)
    col3.selectbox("Select camera", ("Loading Dock", "Processing", "Warehouse"))
    col3.subheader("Camera: Loading Dock")
    col3.metric("Today's Alerts vs Yesterday", todays_alert_values, delta=int(delta))

if select_box == "Report":
    col3, col4 = st.columns([5, 1])
    col3.subheader("Report: Loading Dock")
    col4.selectbox("Select camera", ("Loading Dock", "Processing", "Warehouse"))
    st.markdown("Select date range")
    earlier = today - datetime.timedelta(days=10)
    col3, col4 = st.columns(2)
    start_date = col3.date_input('Start date', earlier)
    end_date = col4.date_input('End date', today)
    if start_date <= end_date:
        df = pd.read_csv('Report.csv', delimiter=';')
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df = df.sort_values(by = 'Date')
        mask = (df['Date'] >= str(start_date)) & (df['Date'] <= str(end_date))
        filtered_dataframe = df.loc[mask]
        filtered_dataframe = filtered_dataframe.sort_values(by = 'Date')
        print(filtered_dataframe['Date'].values)
        date_values = filtered_dataframe['Date'].values
        formatted_date = []
        for i in range(len(date_values)):
            d = dt.strptime(str(date_values[i]), '%Y-%m-%dT%H:%M:%S.%f000').strftime("%Y-%m-%d")
            formatted_date.append(d)
        alert_values = filtered_dataframe['Alerts'].values
        
        filter_df = pd.DataFrame({'Date': formatted_date, 'Alerts': alert_values})
        filter_df = filter_df.rename(columns={'Date':'index'}).set_index('index')

        st.bar_chart(filter_df)
    else:
        st.error('Error: End date must fall after start date.')

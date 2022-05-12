import streamlit as st
import numpy as np
import pandas as pd
import datetime
from datetime import datetime as dt

def show_live_stream(video_feed, csv_file):    
    #get video
    video_file = open(video_feed, 'rb')
    video_bytes = video_file.read()

    #get daily alert ticker
    df = pd.read_csv(csv_file, delimiter=';')
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df = df.sort_values(by = 'Date')
    todays_alerts = (df['Date'] == str(today))
    todays_alerts_dataframe = df.loc[todays_alerts]
    todays_alert_values = todays_alerts_dataframe['Alerts'].values
    
    yesterday = today - datetime.timedelta(days=1)
    yesterdays_alerts = (df['Date'] == str(yesterday))
    yesterdays_alerts_dataframe = df.loc[yesterdays_alerts]
    yesterdays_alert_values = yesterdays_alerts_dataframe['Alerts'].values

    delta = todays_alert_values - yesterdays_alert_values

    return video_bytes, todays_alert_values, delta

def show_report(csv_file):
    st.markdown("Select date range")
    
    earlier = today - datetime.timedelta(days=10)
    
    col_startdate, col_stopdate = st.columns(2)
    start_date = col_startdate.date_input('Start date', earlier)
    end_date = col_stopdate.date_input('End date', today)
    
    if start_date <= end_date:
        df = pd.read_csv(csv_file, delimiter=';')
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df = df.sort_values(by = 'Date')
        
        mask = (df['Date'] >= str(start_date)) & (df['Date'] <= str(end_date))
        
        filtered_dataframe = df.loc[mask]
        filtered_dataframe = filtered_dataframe.sort_values(by = 'Date')
        
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

#general layout settings
st.set_page_config(layout="wide")

#sidebar
col10, col11 = st.sidebar.columns([2, 1])
col10.image("logo.png")
col11.header("   ")
selected_page = st.sidebar.selectbox("Navigation Menu", ("Live Stream", "Report"))

#general variables
today = datetime.date.today()
now = dt.now().strftime("%H:%M:%S")

#visible sections
if selected_page == "Live Stream":
    st.header("Viu More Safety Detection - Live Stream")
    #show date & time
    today_formatted = today.strftime('%d %b %Y')
    st.subheader(str(today_formatted) + " - " + str(now))
    col21, col22, col23 = st.columns([4, 1, 3])
    
    camera_zone = col23.selectbox("Select camera", ("Loading Dock", "Garage"))
    
    if camera_zone == "Loading Dock":
        video_bytes, todays_alert_values, delta = show_live_stream("Loading_Dock.mp4", "Report_Loading_Dock.csv")
        col21.video(video_bytes)
        col22.markdown("")
        col23.subheader("Selected Camera:")
        col23.subheader("Loading Dock - Zone Detection")
        col23.metric("Today's Alerts vs Yesterday", todays_alert_values, delta=int(delta))
    
    elif camera_zone == "Garage":
        video_bytes, todays_alert_values, delta = show_live_stream("Garage.mp4", "Report_Garage.csv")
        col21.video(video_bytes)
        col22.markdown("")
        col23.subheader("Selected Camera:")
        col23.subheader("Garage - Zone Detection")
        col23.metric("Today's Alerts vs Yesterday", todays_alert_values, delta=int(delta))

if selected_page == "Report":
    st.header("Viu More Safety Detection - Report")
    col31, col32 = st.columns([5, 1])
    
    camera_zone = col32.selectbox("Select camera", ("Loading Dock", "Garage"))

    if camera_zone == "Loading Dock":
        col31.subheader("Report: Loading Dock - Zone Detection")
        show_report("Report_Loading_Dock.csv")

    elif camera_zone == "Garage":
        col31.subheader("Report: Garage - Zone Detection")
        show_report("Report_Garage.csv")



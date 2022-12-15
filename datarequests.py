import argparse
import datetime
import os
import sys
import time  # to simulate a real time data, time loop
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
#import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development


def build_dashboard(dfg):
    # Set configuration
    st.set_page_config(
        page_title="DRD",
        page_icon="✅",
        layout="wide",
    )  

    # Title
    st.title("Data Requests Dashboard")

    # Create three columns
    kpi1, kpi2, kpi3 = st.columns(3)
    
    # Fill columns
    count_w = int(dfg[((dfg["State"] == "Open") & (dfg["Labels"] == "Data,Working on it"))]["Labels"].count())
    count_r = int(dfg[((dfg["State"] == "Open") & (dfg["Labels"] == "Data,Ready to test"))]["Labels"].count())

    date_before = datetime.date.today() - datetime.timedelta(days=15)
    df['Closed At (UTC)'] = pd.to_datetime(df['Closed At (UTC)'], format='%Y-%m-%d')
    count_c = int(df[df['Closed At (UTC)'] >= str(date_before)]["State"].count()) 

    title_issueid_c = df[df['Closed At (UTC)'] >= str(date_before)][["Title", "Issue ID", "URL"]]

    kpi1.metric(
        label="Working on it",
        value=int(count_w),
    )
    kpi2.metric(
        label="Ready to test",
        value=int(count_r),
    )
    kpi3.metric(
        label="Closed",
        value=int(count_c),
    )
    st.write("Closed issues: ")
    st.table(title_issueid_c)


# Main ---
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Error. Pass csv file name as argument. Exiting...")
        sys.exit(1)
    else:
        csv_file = sys.argv[1]
        csv = "~/Documents/Margarida/Feina/BSC/datarequests-dashboard_streamlit/" + str(csv_file)

        # Read CSV file to a Data Frame 
        df_gitlab = pd.read_csv(csv_file)  

        # Group by label
        dfg = df_gitlab.groupby(["Title", "Issue ID", "State","Labels"]).size().to_frame(name = 'Count').reset_index()
        df = df_gitlab.groupby(["Title", "Issue ID", "URL", "State","Labels", "Closed At (UTC)"]).size().to_frame(name = 'Count').reset_index()
        print(dfg)

        build_dashboard(dfg)



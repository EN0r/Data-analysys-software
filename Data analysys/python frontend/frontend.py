from numpy import trace
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
# string matching
from thefuzz import fuzz
from thefuzz import process
#------------------------------------------Reasons why i decided to do this project in c# and python -----------------------------------------------------------------------------------------------------
# Quick note: I do not have any prior exentive knowledge in c#(although with the similarities to c++ it was alot easier to pick up than python) and python so i have picked up this knowledge in the few days
# It may be seen as reinventing the wheel since there are tools which can do the same 
# This job does not make use of c# and i am aware of this but im primarily doing it to have a finished and completed project on github and to also show that i can come up with *unusual* solutions to problems and use my programming knowledge to quickly learn new languages.
# Obviously there are already tools such as powerBI which generate reports and insights from gathered data but i started this as i think i've said im super interested into career progression into the data science side and there is alot of crossover into data science from data analysis
# I took this project on more as a challenge to myself to see how far i can get when learning new tech and using programming in conjunction with data filtering and data analysis and i think it is going really well.
# Also have a bad habit with pascalCase naming so i apologize.
#------------------------------------------- Total criteria ----------------------------------------------------------------------------------------------------------------------------------------------
# The value numbers should be presented in GBP (I have included the values for conversion but have not completed this step.) ----- price conversion from gbpunitprice * salesvalue done (if it already gbp it ignores it) in the c# application
# Make sure the dates are displayed correctly (including times if you want to use them) -- Need to display dates in some form or another Maybe a bar graph which shows dates and flights
# Use filters/slicers to allow users to interact with your findings ----- I believe this criteria is ticked with the interactive website
#----------------------------------------------NOT DONE-------------------------------------------------------------------------------------------------------------------------------------------------------
# A final consideration would be to look closely at the Brokers. Enjoy does exist in this list. This means that our prices here are in a different category to others. How might you deal with that? -------- I need to work on this as i only have the data filtering. I need to closely analyse the data with the sales lesser than the sales of enjoy and look at dates
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# game plan num 2
# I NEED to also make a pie chart or something similar maybe for average price of cars being sold across all vendors. So i need to use my c# software to filter the data entries to only vendor and sale price and go through how much in total it averages out to
# need to do a airport count and have a graph for most common airports travelled to


# Similarity checking and what ive found about the data is that there are sites with similarities but they cant be named
# In regards to what is done above the stringmatching function is what i used to learn the fuzz spent like a solid 40 ish mins learning that 
#
#
#
#
#

print("New test below V -------------------------------------------------------")

# Disp
pages = [ "Broker Counts","Travel Count Occurences","Pricing and dates" ] #using arrays in python is rather strange
pageName = st.sidebar.selectbox("Select a page:",pages)

# fuzzy string matching
def stringMatching(nameArray): # Again google is a massive help when looking how to use these packages as a python noob
    grouped = {} # have a group dictionary for matching certainty
    processed = set()
    for name in nameArray:
        if name in processed:
            continue

        matches = process.extract(name,nameArray,scorer=fuzz.token_sort_ratio, limit=None) # using a token sort ratio as im getting obvious outliers in the return data like trip.com being matched with stress free car rental which have no real definitive correlation
        similar = [match[0] for match in matches if match[1] >= 95] # 90 percent certainty whether the two names are the same
        for match in similar:
            processed.add(match)
        grouped[name] = similar
    return grouped


#  ------------------------------------------------------------------------PAGE 1-------------------------------------------------------------------
if pageName == pages[0]:
    # The data below has 2 unnamed columns due to on the data exported the datagridview to count occurence copies the original datagrid view with the two columns it expected from the original even though it was cut down
    # that is a bug which i need to fix eventually if i continue using the exported data from the original. Fortunately plotly gets rid of erreneous data entries it seems.
    st.title("Broker count occurences")
    tsv_file = "data\\brokerOccurenceCount.tsv" 
    df = pd.read_csv(tsv_file, sep="\t") 

    st.dataframe(df)

    # Choose chart type
    chart_type = st.selectbox("Select Chart Type:", ["Bar", "Line"])
    # This code below is to fix erreneous values. I should have 
    df['Value'] = df['Value'].str.strip().str.lower()
    df = df[df['Value'].notna()]
    groupedNames = stringMatching(df['Value'].unique()) # This will get all unique values and add them to an array then send the array to the unction
    print(groupedNames)
    # ^^ data consolidated well

    # invert matches on the returned dictionary to et rue values and combined data
    matches = {}
    for realName, similarNames in groupedNames.items():
        for name in similarNames:
            matches[name] = realName
    df['NormalizedValue'] = df['Value'].map(matches) # edit dataframe and combine values using mapping
    df = df[df['NormalizedValue'].notna()]
    groupedDf = df.groupby("NormalizedValue").sum(numeric_only=True).reset_index()
    groupedDf.rename(columns={"NormalizedValue": "Value"}, inplace=True)
    

    if chart_type == "Bar":
       x_col = "Value"
       y_col = "Count"
       fig = px.bar(groupedDf, x=x_col, y=y_col)
       fig.update_layout(xaxis=dict(tickangle=-90,tickmode='linear',tickfont=dict(size=10))) # force the *unnamed entries to have a tag on the value x axis
    elif chart_type == "Line":
       x_col = "Value"
       y_col = "Count"
       fig = px.line(groupedDf, x=x_col, y=y_col)
       fig.update_layout(xaxis=dict(tickangle=-90,tickmode='linear',tickfont=dict(size=10))) # force the *unnamed entries to have a tag on the value x axis

    st.plotly_chart(fig,use_container_width=True)

    storedVendors = []
    # loop through the data entries in the x row to gather all vendors to add through to the storedVendor array
    for trace in fig['data']: 
        # first time using numpy took me ages to figure this out :()
        if isinstance(trace['x'], np.ndarray):
            vendor_names = trace['x'].tolist() 
        else:
            vendor_names = trace['x'].tolist()  
        for vendorName in vendor_names:
            if vendorName not in storedVendors:
                storedVendors.append(vendorName)

    removeEntriesLesser = st.selectbox("Select vendor to display all vendors with higher occurences",storedVendors)
    options = ["Show only vendors with sales greater than selection.", "Show only vendors with sales lesser than selection."]
    greaterthanOrLesserthan = st.selectbox("Show vendors with greater than or lesser than sales.", options)
    # only show companies with a greater than value of the company selected so it removes data from companies with lower sales.
    updateWithSelection = st.button("Create graph with selected omissions.")
    st.subheader("Graph with included omissions:")


    # -------------- Button press handlin
    if updateWithSelection:
        selected_vendor_count = groupedDf.loc[groupedDf[x_col] == removeEntriesLesser, y_col].values[0]
        if greaterthanOrLesserthan == options[0]:
            # this code below i did have to research around for and look for awnsers online of how to do this in python specifically
           
            if chart_type == "Bar": # To be honest if i put this into a function i could just reuse this rather than rewrite but im only using this  twice. That could still be a little improvement though
                dataframeFilter = groupedDf[groupedDf[y_col] > selected_vendor_count]
                fig = px.bar(dataframeFilter,x=x_col, y=y_col)
            if chart_type == "Line": # Kinda is sad how there's no switch statements :(
                dataframeFilter = groupedDf[groupedDf[y_col] > selected_vendor_count]
                fig = px.bar(dataframeFilter,x=x_col, y=y_col)
            st.plotly_chart(fig,use_container_width=True) # draw a new graph
        # show companies with lesser sales
        if greaterthanOrLesserthan == options[1]:
            dataframeFilter = groupedDf[groupedDf[y_col] < selected_vendor_count]
            if chart_type == "Bar":
                fig = px.bar(dataframeFilter,x=x_col, y=y_col)
            if chart_type == "Line":
                fig = px.bar(dataframeFilter,x=x_col, y=y_col)
            st.plotly_chart(fig,use_container_width=True)
    
    


#Page 2
if pageName == pages[1]:
    st.title("Travel insights and a location heatmap with a date heatmap")
    # ------------------------------------ airport mapping below
    airportoccurenceCount = "data\\locationCount.tsv" 
    dFrame = pd.read_csv(airportoccurenceCount,sep="\t")
    st.dataframe(dFrame)
    # text below
    st.subheader("Locations with data");
    # for mapping the airports on a cool interactive lil map :)
    airport_coords = {
    "Bologna Airport": {"lat": 44.5354, "lon": 11.2887},
    "Palermo Airport": {"lat": 38.1759, "lon": 13.0910},
    "Malaga Airport": {"lat": 36.6749, "lon": -4.4991},
    "Murcia Airport": {"lat": 37.7750, "lon": -1.1250},
    "Grenoble Airport": {"lat": 45.3629, "lon": 5.3294},
    "Dublin Airport": {"lat": 53.4273, "lon": -6.2436},
    "Keflavik International Airport": {"lat": 63.9850, "lon": -22.6056},
    "Lisbon Airport": {"lat": 38.7742, "lon": -9.1342},
    "Podgorica Airport": {"lat": 42.3594, "lon": 19.2519},
    "Beirut Airport": {"lat": 33.8209, "lon": 35.4884}}

    dFrame['latitude'] = dFrame['Value'].map(lambda x: airport_coords.get(x,{}).get("lat"))
    dFrame['longitude'] = dFrame['Value'].map(lambda x: airport_coords.get(x,{}).get("lon"))
    dFrame = dFrame.dropna(subset=["latitude","longitude"])
    figure2 = px.scatter_mapbox(dFrame, lat="latitude",lon="longitude",size="Count",hover_name="Value",hover_data=["Count"],color_discrete_sequence=["blue"],zoom=3,height=600)

    figure2.update_layout(mapbox_style="open-street-map")
    figure2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(figure2, use_container_width=True)

    df = pd.read_csv("data\\dateLocationBrokername.tsv", sep="\t")
   
    # had to google regex here since ive had some difficulties in understanding it.
    df['QueryDateTime'] = df['QueryDateTime'].replace(to_replace=r'^24:', value='00:', regex=True)
    df['QueryDateTime'] = pd.to_datetime(df['QueryDateTime'], errors='coerce')
    df['Hour'] = df['QueryDateTime'].dt.hour
    #kinda sad how streamlit does not support breakpoints 
    df['Minute'] = df['QueryDateTime'].dt.minute

    # to be honest the heatmap on streamlit doesnt look too great
    heatmap_data = df.groupby(['Hour', 'Minute']).size().reset_index(name='Count')
    heatmap_pivot = heatmap_data.pivot(index='Hour', columns='Minute', values='Count').fillna(0)

    # Plotly heatmap
    fig = px.imshow(heatmap_pivot,
                    labels=dict(x="Minute", y="Hour", color="Query Count"),
                    x=heatmap_pivot.columns,
                    y=heatmap_pivot.index,
                    aspect="auto")

    fig.update_layout(title="Heatmap of queries by time")
    st.plotly_chart(fig)

    st.write("Describe the heatmap above");


    # pricing data

    pricingDf = pd.read_csv("data\\brokerDateAndPricing.tsv",sep="\t")
    #temporarily getting rid of the pricing symbol 
    pricingDf['SalePrice'] = pricingDf['SalePrice'].replace(to_replace=r'£', value='', regex=True).astype(float)



#Page 3 -- analysis of the final product using figures ect :I
if pageName == pages[2]:
    st.title("My final analysis of the data displayed.")
    



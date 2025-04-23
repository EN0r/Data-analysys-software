from os import write
from numpy import trace
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
# string matching
from thefuzz import fuzz
from thefuzz import process
# Image rendering

from PIL import Image

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
pages = [ "Broker Counts","Travel Count Occurences","What I think was important from this?" ] #using arrays in python is rather strange
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
    # Subheading and writing.

    st.subheader("What I could do better with these graphs?")
    st.write('''
    During this I had to google possible solutions to problems I had encountered such as some data could also be combined due to the scraper gathering stressfreecarrental.com
    and stress free car rental and I had to google how I could actually figure this out as it’s a problem I’ve never had to deal with prior to today and I found out its called
    *Fuzzy string matching* which is a common 
    issue to deal with in data analytics. This is a problem I never thought I had to deal with as in truth I had never heard of it. I have decided to implement 
    fuzzy string matching using the python package TheFuzz to determine if strings are close enough to be combined into one piece of data. The reason why i could have done
    this better is that I could have used more advanced python packages to perhaps automate it using machine learning et cetera. Also, In the c# software I could have handled erroneous data better
    and made sure there was not a empty box being counted by the count occurence section of that software.
    ''')
    
    


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

    figure2.update_layout(mapbox_style="open-street-map") # link it to plotlys map system
    figure2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(figure2, use_container_width=True)
    st.subheader("What does this map mean?")
    st.write('''
    This map shows the most popular location across all companies on the data set using count occurences and it shows that Lisbon airport has the largest
    amount of car hires for that specific destination. This is interesting because the most common holidays I thought would be from Spain from the dataset.
    I guess it goes to show that data means everything and sometimes it defeats expectations.

    Note:
    The larger the spots on the map means there are more customers who hire cars for that destination.
    ''')




    # ----- location heatmap section

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
    fig = px.imshow(heatmap_pivot,labels=dict(x="Minute", y="Hour", color="Query Count"),x=heatmap_pivot.columns,y=heatmap_pivot.index,aspect="auto")
    fig.update_layout(title="Heatmap of queries by time")
    st.plotly_chart(fig)

    st.subheader("What this heatmap shows?")
    st.write('''
        This data heatmap shows that there are no car hires from 22:52pm until 00:32am.
        Also interesting how midday (11:21 and 1:32am) have over 5000 queries during that time. 
        Perhaps that aligns with most common flight times. And there aren’t any specific dates in the dataset only just times.
    ''')


    # pricing data

    pricingDf = pd.read_csv("data\\brokerDateAndPricing.tsv",sep="\t")
    st.dataframe(pricingDf)
    #temporarily getting rid of the pricing symbol 
    pricingDf['SalePrice'] = pricingDf['SalePrice'].replace(to_replace=r'£', value='', regex=True).astype(float)
    selected_brokers = st.multiselect("Select Brokers to Compare",options=pricingDf['BrokerName'].unique(),default=pricingDf['BrokerName'].unique())# allow the option to compare two brokers and pricing
    # data filtering like the groupeddf earlier
    filtered_df = pricingDf[pricingDf['BrokerName'].isin(selected_brokers)]
    #average sale pricing
    avg_prices = filtered_df.groupby('BrokerName')['SalePrice'].mean().reset_index()
    fig = px.bar(avg_prices,x='BrokerName',y='SalePrice',color='BrokerName',title="Average Sale Price by Broker",labels={'SalePrice': 'Average Price (£)', 'BrokerName': 'Broker'},height=500)
    fig.update_layout(xaxis=dict(tickangle=-90,tickmode='linear',tickfont=dict(size=10)),xaxis_title="Broker", yaxis_title="Average Sale Price (£)", showlegend=False)
    st.plotly_chart(fig)

    st.subheader("**Quick analysys of the data.**")
    st.write('''
         Averages are skewed due to original erroneous data showing up in the original dataset.
         I am very sure that auto Europe does not rent out cars for 79,000gbp? So that’s some anomalistic data.
         This is interesting as in my own homebrew software it did not pick up this data and i had even tried excels highest to lowest data sorting and it
         never actually picked this up. This genuinely piques my curiosity over what is causing this data. I had originally thought
         integer overflow but disregarded it as 32 bit+ systems interger overflow are 2.147b so it is unlikely.

         Also, Enjoy travel group (as a whole) has a average price of 494GBP per sale which is actually competing with large global companies such as enterprise car hire and also easyCar which is 
         interesting as these companies are far larger than enjoytravel which is really impressive.
    ''')

if pageName == pages[2]:
    st.header("What I think was important from this data?")
    images = ["images/anomalisticData.png", "images/heatmap.png","images/enjoytravelCompetition.png","images/enjoyGraph.png","images/mapGraph.png"]
    st.image(images[0],caption="Anomalistic pricing data", use_container_width=True)
    st.write('''
    One thing i think was important was pinpointing anomalistic data from the use of data analysis tools and making sure that theres some sort of manual sift
    through the data(even if it is quick) as alot of common tools can not pick such anomalies up like the one you see above. For some reason in the original dataset
    the webscraper picked up that. Primarily because these anomalies skew data heavily such as what was seen in the graph on the other page where Autoeurope had a
    average sale of over 4000 pounds. Excel and even my own custom tools did not pick up this pricing issue even when filtering highest price to lowest
    and had caused me to manually search it to prevent this data being picked up even after being filtered in data filtering!
    ''')

    st.subheader("Why is the most common car hire at 11:39 to 00:56?")
    st.image(images[1], use_container_width=True)
    st.write('''
    This was a question I raised to myself based on the heatmap that i had created to visualize data on the other page. It seems
    that this is due to those times seeming to be the most common flight times for the clientelle(researched as the data itself did not represent this).
    ''')
    st.subheader("Who is enjoy travel competing with?")
    st.image(images[2],caption="Due to a lack of effective fuzzy string matching in conjunction to machine learning algorithms it has three bars that I manually averaged out enjoy travels figures and represented it as a white line.", use_container_width=True)
    st.write('''
    From the start of embarking on this project that was actually the first question I had for myself and I think enjoy travel has as a business as it expands.
    On the graph I have the white line showing the average of 494GBP enjoy travel has for its car hires. This graph shows that enjoy travel is actually competing with the more high end businesses in regards to
    average price per sale. This is impressive as companies such as enterprise which you can commonly see their vans around and enjoy travel are managing to sell cars often enough to have a high average price per vehicle despite not being a global corporation.
    Additionally, EnjoyTravel actually beats them in global car hire even without average prices and it does not even include the other webscraped queries such as "enjoyTravel" and "enjoy Car Hire" which gives highly
    valuable insights to who the business is truly competing. This can be seen in the figure below.
    ''')
    st.image(images[3], use_container_width=True)

    st.subheader("Why does the map data representation mean alot?")
    st.image(images[4], use_container_width=True)
    st.write('''
    This data may seem minimal at first but actually seems to give alot of insight to a business as it shows that lisbon airport, spain, dublin and italy are the major players in regards to car hire.
    It can give alot of insight due to the fact that it displays clearly the regions and the clientelle who use car hires which seem to be primarily holiday makers.
    ''')
    st.subheader("Why did I decide to create this and what else could provide insights?")
    st.write('''
    There is alot more that I wish I could have given a overview of if it were not for not taking up all your time(you can probably tell i've spent far too long on this). For example, Using the data
    from the acriss groups on the dataset along side count occurence to see what car is the most common to hire. This can lead to insights such as: "Who hires this car? Families? Solo travellers? Duo travellers? Big groups?" depending
    on the acriss group in general and how much they are going to spend on each trip. Also, with the suppliers it raises the question "Per region who is the most common supplier?" I believe you would want to know that because
    it would be beneficial to have direct ties to the supplies for each region to lower booking prices and potentially widen industry relations with regional car hire services which enjoyTravel has not already connected with and even which car suppliers
    deal with only Euros and not GBP.
    ''')
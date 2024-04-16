import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
from PIL import Image

ico = Image.open("Data/Social_Buzz_Logo.png")

st.set_page_config(layout='wide',page_icon=ico)

st.title('BUZZ @ Social Buzz')
st.divider()


################# Reading Data File #################
coords = pd.read_csv("Data/Final Coordinates.csv")
all_data = pd.read_csv('Data/Data.csv')
age_data = all_data[all_data['Age_Bucket']!='Less than 13']
alt_data = all_data[all_data['State_Code']!='Overseas Location']


####################################### Creating a map for understanding geographical distribution  #######################################
#creating a dictionary to fetch the statenames
stat_code = {}
for x in coords['city_code']:
    stat_code[x] = (coords[coords['city_code']==x]['city'].tolist()[0])
stat_code['Overseas Location'] = 'Overseas Location'



geo = st.container(border=True)
geo_chart,geo_des = geo.columns([.70,.30])
geo_des_ = geo_des.container(border=True)
geo_chart_ = geo_chart.container(border=True)

geo_des_.write('WHAT TO PRODUCE?')
geo_des_.markdown('<div style="text-align: justify; font-size: 16px">By leveraging the insights provided by this dashboard, content creators can optimize their social media content strategy by producing the most engaging content types within the most consumed categories. This section visualizes the consumption patterns of different content categories and provides percentage breakdowns of content consumption to identify the most engaging category.</div>',unsafe_allow_html=True)
geo_des_.write('\n')
geo_des_.markdown('<div style="text-align: justify; font-size: 16px">As such, it identifies emerging trends and topics that resonate with the audience (based on their demographics) and enables proactive content planning by predicting future trends based on historical data analysis.</div>',unsafe_allow_html=True)
geo_des_.write('\n')

geo_metric = geo_des_.selectbox('Select Evaluation Metric:',['Number of Reactions/Interactions','Average Duration Spent',
                                         'Ratio of Postive/Negative Sentiments','Ratio of Neutral/Negative Sentiments',
                                         'Number of Unqiue Users Interacting'],key=6)

#a function that gives us relevant feedback
def geo_data_thrower(metric):
    if metric == 'Number of Reactions/Interactions':
        dat = alt_data.groupby(['State_Code'])['Reaction ID'].count().sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Reaction ID':'Users Interaction/Reacting'},inplace=True)
        dat_ = alt_data.groupby(['State_Name'])['Reaction ID'].count().sort_values(ascending=False)
        dat_ = pd.DataFrame(dat_)
        dat_.rename(columns={'Reaction ID':'Users Interaction/Reacting'},inplace=True)
        return dat,dat_
    elif metric == 'Average Duration Spent':
        dat = alt_data.groupby(['State_Code'])['Duration'].mean().round(2).sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Duration':'Average Duration'},inplace=True)
        dat_ = alt_data.groupby(['State_Name'])['Duration'].mean().round(2).sort_values(ascending=False)
        dat_ = pd.DataFrame(dat_)
        dat_.rename(columns={'Duration':'Average Duration'},inplace=True)
        return dat,dat_
    elif metric == 'Ratio of Postive/Negative Sentiments':
        slice_1 = alt_data.groupby(['State_Code','Sentiment'])['Reaction ID'].count().unstack()
        dat = (slice_1['positive']/slice_1['negative']).round(2).sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={0:'Ratio of Postive to Negative Sentiments'},inplace=True)
        slice_2 = alt_data.groupby(['State_Name','Sentiment'])['Reaction ID'].count().unstack()
        dat_ = (slice_2['positive']/slice_2['negative']).round(2).sort_values(ascending=False)
        dat_ = pd.DataFrame(dat_)
        dat_.rename(columns={0:'Ratio of Postive to Negative Sentiments'},inplace=True)
        return dat,dat_
    elif metric == 'Ratio of Neutral/Negative Sentiments':
        slice_1 = alt_data.groupby(['State_Code','Sentiment'])['Reaction ID'].count().unstack()
        dat =  (slice_1['neutral']/slice_1['negative']).round(2).sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={0:'Ratio of Neutral to Negative Sentiments'},inplace=True)
        slice_2 = alt_data.groupby(['State_Name','Sentiment'])['Reaction ID'].count().unstack()
        dat_ =  (slice_2['neutral']/slice_2['negative']).round(2).sort_values(ascending=False)
        dat_ = pd.DataFrame(dat_)
        dat_.rename(columns={0:'Ratio of Neutral to Negative Sentiments'},inplace=True)        
        return dat,dat_
    elif metric == 'Number of Unqiue Users Interacting':
        dat = alt_data.groupby(['State_Code'])['Reaction ID'].nunique().sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Reaction ID':'Number of Unique Users'},inplace=True)
        dat_ = alt_data.groupby(['State_Name'])['Reaction ID'].nunique().sort_values(ascending=False)
        dat_ = pd.DataFrame(dat_)
        dat_.rename(columns={'Reaction ID':'Number of Unique Users'},inplace=True)        
        return dat,dat_

#arranging the dataframes
map_dat_1, map_dat_2 = geo_data_thrower(geo_metric)
map_dat_1.reset_index(inplace=True)

map_dat_1['State_Name'] = map_dat_1['State_Code'].apply(lambda x: stat_code[x])


# Extracting data from the CSV
states = map_dat_1['State_Code'].values
users = map_dat_1[map_dat_1.columns.tolist()[1]].values
state_names = map_dat_1["State_Name"].values


#For plotting the map
# Constructing hover text
hover_text = [f'State: {state_name}<br>Selected Metric: {user}' for state_name, user in zip(state_names, users)]
# Creating the data dictionary for the choropleth map
data = dict(
    type='choropleth',
    colorscale='Viridis',
    reversescale=True,
    locations=states,
    locationmode='USA-states',
    z=users,
    colorbar={'title': 'Metric'},
    hoverinfo='text',
    text=hover_text
)
# Creating layout
layout = dict(
    title='State-Wise Distribution of Users and Trends in User Behaviour',
    geo=dict(
        scope='usa',
        projection=dict(type='albers usa'),
        showlakes=True,
        lakecolor='rgb(255, 255, 255)',
    ),
)


# Creating the figure
choromap = go.Figure(data=[data], layout=layout)
geo_chart_.plotly_chart(choromap)   


############################################################## What kind of data to produce ##############################################################
what_space = st.container(border=True)
what_des,what_chart = what_space.columns([.30,.70])
what_des_ = what_des.container(border=True)
what_chart_ = what_chart.container(border=True)

#Description Section
what_des_.write('WHAT TO PRODUCE?')
what_des_.markdown('<div style="text-align: justify; font-size: 16px">By leveraging the insights provided by this dashboard, content creators can optimize their social media content strategy by producing the most engaging content types within the most consumed categories. This section visualizes the consumption patterns of different content categories and provides percentage breakdowns of content consumption to identify the most engaging category.</div>',unsafe_allow_html=True)
what_des_.write('\n')
what_des_.markdown('<div style="text-align: justify; font-size: 16px">As such, it identifies emerging trends and topics that resonate with the audience (based on their demographics) and enables proactive content planning by predicting future trends based on historical data analysis.</div>',unsafe_allow_html=True)
what_des_.write('\n')
what_based_metric = what_des_.selectbox('Select Evaluation Metric:',['Number of Reactions/Interactions','Average Duration Spent',            
                                         'Ratio of Postive/Negative Sentiments','Ratio of Neutral/Negative Sentiments',
                                         'Number of Unqiue Users Interacting'],key=1)

#function to fetch data based on the nature if analysis asked for 
def what_data_thrower(metric):
    if metric == 'Number of Reactions/Interactions':
        dat = age_data.groupby(['Category'])['Reaction ID'].count().sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Reaction ID':'Users Interaction/Reacting'},inplace=True)
        return dat
    elif metric == 'Average Duration Spent':
        dat = age_data.groupby(['Category'])['Duration'].mean().round(2).sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Duration':'Average Duration in Minutes'},inplace=True)
        return dat
    elif metric == 'Ratio of Postive/Negative Sentiments':
        slice_1 = age_data.groupby(['Category','Sentiment'])['Reaction ID'].count().unstack()
        dat = (slice_1['positive']/slice_1['negative']).round(2).sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={0:'Ratio of Postive to Negative Sentiments'},inplace=True)
        return dat
    elif metric == 'Ratio of Neutral/Negative Sentiments':
        slice_1 = age_data.groupby(['Category','Sentiment'])['Reaction ID'].count().unstack()
        dat =  (slice_1['neutral']/slice_1['negative']).round(2).sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={0:'Ratio of Neutral to Negative Sentiments'},inplace=True)
        return dat
    elif metric == 'Number of Unqiue Users Interacting':
        dat = age_data.groupby(['Category'])['Reaction ID'].nunique().sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Reaction ID':'Number of Unique Users'},inplace=True)
        return dat

#prepping the data returned from function for plotting
req_what_data = what_data_thrower(what_based_metric)
req_what_data.reset_index(inplace=True )
#plotting the barplot for further analysis
what_based_chart = px.bar(req_what_data,color='Category',x='Category',
                         y=req_what_data.columns.tolist()[1],title='What kind of content should we produce, where is the most scope?')
what_chart_.plotly_chart(what_based_chart)





############################################################## Age Related Analysis ##############################################################
whom_space = st.container(border=True)
whom_space_chart,whom_space_des = whom_space.columns([.70,.30])
whom_space_des_ = whom_space_des.container(border=True)
whom_space_chart_ = whom_space_chart.container(border=True)

whom_space_des_.write('FOR WHOM TO PRODUCE?')
whom_space_des_.markdown('<div style="text-align: justify; font-size: 16px">Our Social Media Audience Analytics Dashboard empowers content creators and marketers with invaluable insights into audience demographics and monetization potential, enabling targeted content production and optimization strategies. It analyzes the age distribution of the audience to identify which age groups hold the highest monetization potential.</div>',unsafe_allow_html=True)
whom_space_des_.write('\n')
whom_space_des_.markdown('<div style="text-align: justify; font-size: 16px"> It also provides insights into the purchasing power, interests, and engagement levels of different age demographics. Content strategies can then be tailored to resonate with the demographics that are most interested in particular themes. As such, it guides content creators in developing sponsorship deals, advertising campaigns, and product placements targeted at specific audience segments.</div>',unsafe_allow_html=True)
whom_space_des_.write('\n')
age_based_metric = whom_space_des_.selectbox('Select Evaluation Metric:',['Number of Reactions/Interactions','Average Duration Spent',
                                         'Ratio of Postive/Negative Sentiments','Ratio of Neutral/Negative Sentiments',
                                         'Number of Unqiue Users Interacting'])


#function to fetch data based on the nature if analysis asked for
def age_data_thrower(metric):
    if metric == 'Number of Reactions/Interactions':
        dat = age_data.groupby(['Age_Bucket'])['Reaction ID'].count().sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Reaction ID':'Users Interaction/Reacting'},inplace=True)
        return dat
    elif metric == 'Average Duration Spent':
        dat = age_data.groupby(['Age_Bucket'])['Duration'].mean().round(2).sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Duration':'Average Duration in Minutes'},inplace=True)
        return dat
    elif metric == 'Ratio of Postive/Negative Sentiments':
        slice_1 = age_data.groupby(['Age_Bucket','Sentiment'])['Reaction ID'].count().unstack()
        dat = (slice_1['positive']/slice_1['negative']).round(2).sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={0:'Ratio of Postive to Negative Sentiments'},inplace=True)
        return dat
    elif metric == 'Ratio of Neutral/Negative Sentiments':
        slice_1 = age_data.groupby(['Age_Bucket','Sentiment'])['Reaction ID'].count().unstack()
        dat =  (slice_1['neutral']/slice_1['negative']).round(2).sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={0:'Ratio of Neutral to Negative Sentiments'},inplace=True)
        return dat
    elif metric == 'Number of Unqiue Users Interacting':
        dat = age_data.groupby(['Age_Bucket'])['Reaction ID'].nunique().sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Reaction ID':'Number of Unique Users'},inplace=True)
        return dat

#preping the data for the bar chart   
req_age_data = age_data_thrower(age_based_metric)
req_age_data.reset_index(inplace=True )
#creating a barchart and plotting the same
age_based_chart = px.bar(req_age_data,color='Age_Bucket',x='Age_Bucket',
                         y=req_age_data.columns.tolist()[1],title='What Age Group to Target as Content Creators?')
whom_space_chart_.plotly_chart(age_based_chart)


############################################################## When Analysis ##############################################################
when_hour_space = st.container(border=True)
when_hour_space_des,when_hour_space_chart = when_hour_space.columns([.30,.70])
when_hour_space_des_ = when_hour_space_des.container(border=True)
when_hour_space_chart_ = when_hour_space_chart.container(border=True)


when_hour_space_des_.write('WHEN IS THE GOLDEN HOUR?')
when_hour_space_des_.markdown('<div style="text-align: justify; font-size: 16px">This section provides invaluable insights into the optimal timing for product or feature launches based on sentiment analysis and audience demographics. These help analyze social media sentiment trends in a day to identify periods with the most positive sentiment and help determine the best timing for product or feature launches to capitalize on those and maximize engagement</div>',unsafe_allow_html=True)
when_hour_space_des_.write('\n')
when_hour_space_des_.markdown('<div style="text-align: justify; font-size: 16px">It identifies peak engagement times for different audience demographics, highlighting when they are most active and receptive to content and assists in scheduling content releases and launch announcements during times when the target audience is most likely to be online and engaged. By leveraging the insights provided by this dashboard, content creators can strategically plan their product or feature launches to coincide with times of positive sentiment and peak audience engagement, ultimately increasing the success and impact of their marketing efforts.</div>',unsafe_allow_html=True)
when_hour_space_des_.write('\n')
#function to fetch data based on the nature if analysis asked for
when_hour_metric = when_hour_space_des_.selectbox('Select Evaluation Metric:',['Number of Reactions/Interactions','Average Duration Spent',
                                         'Ratio of Postive/Negative Sentiments','Ratio of Neutral/Negative Sentiments',
                                         'Number of Unqiue Users Interacting'],key=3)


#function to fetch data based on the nature if analysis asked for
def hour_data_thrower(metric):
    if metric == 'Number of Reactions/Interactions':
        dat = age_data.groupby(['Hour_of_the_day'])['Reaction ID'].count().sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Reaction ID':'Users Interaction/Reacting'},inplace=True)
        return dat
    elif metric == 'Average Duration Spent':
        dat = age_data.groupby(['Hour_of_the_day'])['Duration'].mean().round(2).sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Duration':'Average Duration in Minutes'},inplace=True)
        return dat
    elif metric == 'Ratio of Postive/Negative Sentiments':
        slice_1 = age_data.groupby(['Hour_of_the_day','Sentiment'])['Reaction ID'].count().unstack()
        dat = (slice_1['positive']/slice_1['negative']).round(2).sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={0:'Ratio of Postive to Negative Sentiments'},inplace=True)
        return dat
    elif metric == 'Ratio of Neutral/Negative Sentiments':
        slice_1 = age_data.groupby(['Hour_of_the_day','Sentiment'])['Reaction ID'].count().unstack()
        dat =  (slice_1['neutral']/slice_1['negative']).round(2).sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={0:'Ratio of Neutral to Negative Sentiments'},inplace=True)
        return dat
    elif metric == 'Number of Unqiue Users Interacting':
        dat = age_data.groupby(['Hour_of_the_day'])['Reaction ID'].nunique().sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Reaction ID':'Number of Unique Users'},inplace=True)
        return dat

#preping the data for the bar chart   
req_hour_data = hour_data_thrower(when_hour_metric)
req_hour_data.reset_index(inplace=True )
#creating a barchart and plotting the same
when_hour_based_chart = px.bar(req_hour_data,color='Hour_of_the_day',x='Hour_of_the_day',
                         y=req_hour_data.columns.tolist()[1],title='What is the Golden hour for Content Creators, when is it ideal to post something?')
when_hour_space_chart_.plotly_chart(when_hour_based_chart)


############################################################## When Analysis 2 ##############################################################

when_day_space = st.container(border=True)
when_day_space_chart,when_day_space_des = when_day_space.columns([.70,.30])
when_day_space_des_ = when_day_space_des.container(border=True)
when_day_space_chart_ = when_day_space_chart.container(border=True)

when_day_space_des_.write('WHEN IS THE BEST DAY IN A WEEK?')
when_day_space_des_.markdown('<div style="text-align: justify; font-size: 16px">This section analyzes audience engagement data to identify the most favorable days for content production and publication and provides recommendations on which days of the week are best suited for maximizing reach and engagement. It enables targeted content planning and product launches tailored to specific demographic groups on their most active days.</div>',unsafe_allow_html=True)
when_day_space_des_.write('\n')
when_day_space_des_.markdown('<div style="text-align: justify; font-size: 16px">As such, it determines the ideal day for launching new products or features based on historical engagement trends and audience behavior. Thereby, helping creators maximize visibility and impact by scheduling launches on days when the target audience is most active.</div>',unsafe_allow_html=True)
when_day_space_des_.write('\n')


day_metric = when_day_space_des_.selectbox('Select Evaluation Metric:',['Number of Reactions/Interactions','Average Duration Spent',
                                         'Ratio of Postive/Negative Sentiments','Ratio of Neutral/Negative Sentiments',
                                         'Number of Unqiue Users Interacting'],key=10)


#function to fetch data based on the nature if analysis asked for
def day_data_thrower(metric):
    if metric == 'Number of Reactions/Interactions':
        dat = age_data.groupby(['Day_of_the_week'])['Reaction ID'].count().sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Reaction ID':'Users Interaction/Reacting'},inplace=True)
        return dat
    elif metric == 'Average Duration Spent':
        dat = age_data.groupby(['Day_of_the_week'])['Duration'].mean().round(2).sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Duration':'Average Duration in Minutes'},inplace=True)
        return dat
    elif metric == 'Ratio of Postive/Negative Sentiments':
        slice_1 = age_data.groupby(['Day_of_the_week','Sentiment'])['Reaction ID'].count().unstack()
        dat = (slice_1['positive']/slice_1['negative']).round(2).sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={0:'Ratio of Postive to Negative Sentiments'},inplace=True)
        return dat
    elif metric == 'Ratio of Neutral/Negative Sentiments':
        slice_1 = age_data.groupby(['Day_of_the_week','Sentiment'])['Reaction ID'].count().unstack()
        dat =  (slice_1['neutral']/slice_1['negative']).round(2).sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={0:'Ratio of Neutral to Negative Sentiments'},inplace=True)
        return dat
    elif metric == 'Number of Unqiue Users Interacting':
        dat = age_data.groupby(['Day_of_the_week'])['Reaction ID'].nunique().sort_values(ascending=False)
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Reaction ID':'Number of Unique Users'},inplace=True)
        return dat

#preping the data for the bar chart   
req_day_data = day_data_thrower(day_metric)
req_day_data.reset_index(inplace=True )
#creating a barchart and plotting the same
day_based_chart = px.bar(req_day_data,color='Day_of_the_week',x='Day_of_the_week',
                         y=req_day_data.columns.tolist()[1],title='Which is the best day to post on as a content creator?')
when_day_space_chart_.plotly_chart(day_based_chart)


############### Device Related Analysis ###################
which_device = st.container(border=True)
which_device_des,which_device_chart = which_device.columns([.30,.70])
which_device_des_ = which_device_des.container(border=True)
which_device_chart_ = which_device_chart.container(border=True)

which_device_des_.write('WHAT DEVICES CAN WE COLLABORATE WITH?')
which_device_des_.markdown('<div style="text-align: justify; font-size: 16px">This section provides actionable insights into the devices most commonly used by active users of the platform, offering opportunities for strategic partnerships and expansion. User data has been analyzed to determine the distribution of active users across different device types and helps identify the primary devices preferred by the audience for accessing the platform.</div>',unsafe_allow_html=True)
which_device_des_.write('\n')
#which_device_des_.markdown('<div style="text-align: justify; font-size: 16px">As such, it determines the ideal day for launching new products or features based on historical engagement trends and audience behavior. Thereby, helping creators maximize visibility and impact by scheduling launches on days when the target audience is most active.</div>',unsafe_allow_html=True)
#which_device_des_.write('\n')
dev_based_metric = which_device_des_.selectbox('Select Evaluation Metric:',['Number of Reactions/Interactions','Average Duration Spent',
                                         'Ratio of Postive/Negative Sentiments','Ratio of Neutral/Negative Sentiments',
                                         'Number of Unqiue Users Interacting'],key=80)



def dev_data_thrower(metric):
    if metric == 'Number of Reactions/Interactions':
        dat = age_data.groupby(['Device'])['Reaction ID'].count()
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Reaction ID':'Users Interaction/Reacting'},inplace=True)
        return dat
    elif metric == 'Average Duration Spent':
        dat = age_data.groupby(['Device'])['Duration'].mean().round(2)
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Duration':'Average Duration in Minutes'},inplace=True)
        return dat
    elif metric == 'Ratio of Postive/Negative Sentiments':
        slice_1 = age_data.groupby(['Device','Sentiment'])['Reaction ID'].count().unstack()
        dat = (slice_1['positive']/slice_1['negative']).round(2)
        dat = pd.DataFrame(dat)
        dat.rename(columns={0:'Ratio of Postive to Negative Sentiments'},inplace=True)
        return dat
    elif metric == 'Ratio of Neutral/Negative Sentiments':
        slice_1 = age_data.groupby(['Device','Sentiment'])['Reaction ID'].count().unstack()
        dat =  (slice_1['neutral']/slice_1['negative']).round(2)
        dat = pd.DataFrame(dat)
        dat.rename(columns={0:'Ratio of Neutral to Negative Sentiments'},inplace=True)
        return dat
    elif metric == 'Number of Unqiue Users Interacting':
        dat = age_data.groupby(['Device'])['Reaction ID'].nunique()
        dat = pd.DataFrame(dat)
        dat.rename(columns={'Reaction ID':'Number of Unique Users'},inplace=True)
        return dat
#getting the df ready 
req_dev_data = dev_data_thrower(dev_based_metric)
req_dev_data.reset_index(inplace=True )
#getting the plot for devices ready
dev_based_chart = px.bar(req_dev_data,color='Device',x='Device',
                         y=req_dev_data.columns.tolist()[1],title='What device companies can we colaborate with?')
which_device_chart_.plotly_chart(dev_based_chart)




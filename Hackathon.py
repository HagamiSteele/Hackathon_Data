import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

@st.cache_data  # Cache the function to enhance performance
def load_data():
    
    # Load the CSV file into a pandas dataframe
    df = pd.read_csv('https://raw.githubusercontent.com/HagamiSteele/Hackathon_Data/679f4107e177dc839e6ef0be62fdce31d6e797ae/global_youtube_data_2023.csv')

    # Create age groups and add as a new column
    bin_edges = [1, 21, 101, 201, 301, 401, 501, 601, 701, 801, 901, 996]
    bin_labels = ['1-20', '21-100', '101-200', '201-300', '301-400', '401-500', '501-600', '601-700', '701-800', '801-900', '901-996']
    df['rank_group'] = pd.cut(df['rank'], bins=bin_edges, labels=bin_labels, right=False)

    df.category.fillna('Others', inplace=True)
    df.channel_type.fillna('Others', inplace=True)

    return df

#Load the data using the defined function
df = load_data()
# df.head(5)
# df.category



st.title("Youtube Channel Statistics 😁🎈📈")
st.sidebar.header("Filters")

# Introduction

# Youtube Channel Data and Statistics 


st.markdown("""
            With Youtube being one of the largest platforms on the planet, along with it being a large amount of people's daily lives, it can be important to understand the general distribution of interest on the patform.
""")
with st.expander("📊 **Objective**"):
                 st.markdown("""
The objective of this page is to create a generalized overview of the largest channels on Youtube, as well as their subscribers and characteristics. This is done specifically by analysing categories, uploads, and total subscriber counts.
"""
)
                             
# Tutorial Expander
with st.expander("How to Use the Dashboard 📚"):
    st.markdown("""
    1. **Filter Data** - Use the sidebar filters to narrow down specific data sets.
    2. **Visualize Data** - From the dropdown, select a visualization type to view patterns.
    3. **Insights & Recommendations** - Scroll down to see insights derived from the visualizations and actionable recommendations.
    """)



# Sidebar filter: Age Group
selected_yotube_rank = st.sidebar.multiselect("Select Ranking", df['rank_group'].unique().tolist(), default=df['rank_group'].unique().tolist())
if not selected_yotube_rank:
    st.warning("Please select a from the sidebar")
    st.stop()
filtered_df = df[df['rank_group'].isin(selected_yotube_rank)]


# Sidebar filter: channel_type
selected_channel_types = df['channel_type'].unique().tolist()
selected_channel_types = st.sidebar.multiselect("Select Channel Types", selected_channel_types, default=selected_channel_types)
if not selected_channel_types:
    st.warning("Please select a channel_type from the sidebar")
    st.stop()
filtered_df = filtered_df[filtered_df['channel_type'].isin(selected_channel_types)]

# Sidebar filter: Last Month's views range
min_views = int(df['video_views_for_the_last_30_days'].min())
max_views = int(df['video_views_for_the_last_30_days'].max())
income_range = st.sidebar.slider("Select Last Month's Views", min_views, max_views, (min_views, max_views))
filtered_df = filtered_df[(filtered_df['video_views_for_the_last_30_days'] >= income_range[0]) & (filtered_df['video_views_for_the_last_30_days'] <= income_range[1])]

# Sidebar filter: Total Subscribers
min_subs = int(df['subscribers'].min())
max_subs = int(df['subscribers'].max())
income_range = st.sidebar.slider("Select Subscriber Range ", min_subs, max_subs, (min_subs, max_subs))
filtered_df = filtered_df[(filtered_df['subscribers'] >= income_range[0]) & (filtered_df['subscribers'] <= income_range[1])]


# df.columns

# Dropdown to select the type of visualization
visualization_option = st.selectbox(
    "Select Visualization 🎨", 
    ["Subscribers in Grouped Youtube Rank",
     "Subscribers by Category",
     "Ranking by Number of Uploads",
     "Channel in each Category"]
)
# Visualizations based on user selection
if visualization_option == "Subscribers in Grouped Youtube Rank":
    # Bar chart for Rank Grouping and Number of Subscribers
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x='rank_group',
        y='subscribers',
    ).properties(
        title='Subscribers by Rank Group'
    )
    st.altair_chart(chart, use_container_width=True) 

elif visualization_option == "Subscribers by Category":
    # Bar chart for Category and Number of Subscribers
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x='subscribers',
        y='category',
    ).properties(
        title='Subscribers by Rank Group'
    )
    st.altair_chart(chart, use_container_width=True)       

elif visualization_option == "Ranking by Number of Uploads":
# Boxplot for Ranking by Number of Uploads
    fig, ax = plt.subplots(1,2, figsize =(15,7))

    sns.boxplot(x="rank_group", y="uploads", data=filtered_df, ax=ax[0], palette='Set2')
    ax[0].set_title('Ranking by Number of Uploads')
    ax[0].set_xlabel('Ranking')
    ax[0].set_ylabel('Number of Uploads')
    
    plt.tight_layout()
    st.pyplot(fig)

elif visualization_option == "Channel in each Category":

    # KDE plot for Distance from Home based on Attrition

    plt.figure(figsize=(10, 6))

    sns.histplot(data=filtered_df, y='category', kde=False).set_title('Distribution of channels in categorys')

    plt.xlabel('Numbers of channels in each category')

    plt.ylabel('Different categories')

    plt.title('Bar chart of numbers of channels in each category')

    st.pyplot(plt)

# Display dataset overview
st.header("Dataset Overview")
st.dataframe(df.describe())


# Insights from Visualization Section Expander
with st.expander("Insights from Visualization 🧠"):
    st.markdown("""
    1. **Subscribers in grouped Youtube Rank** - Number of subscribers in each grouping of ranks.
    2. **Subscribers by Category** - Bar chart showing the number of subscribers in each of the given categories, where the "Others" category is a grouping of the non-defined ones.
    3. **Ranking by Number of Uploads** - 'To optimally view the boxplot, it is recommended that you change the "views" slider to a smaller interval.
    4. **Channel in each Category** - A bar chart showing the number of channels in each category, where the "Others" category is a grouping of the non-defined ones.
    """)


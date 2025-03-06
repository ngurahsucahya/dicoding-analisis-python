import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    day = pd.read_csv("clean_day.csv")
    hour = pd.read_csv("clean_hour.csv")
    return day, hour

day,hour = load_data()

month_pivot = day.pivot_table(values='count', index='month', aggfunc='sum').reset_index()
season_pivot = day.pivot_table(values='count', index='season', aggfunc='sum').reset_index()
weather_pivot = day.pivot_table(values='count', index='weather_situation', aggfunc='sum').reset_index()
hour_pivot = hour.pivot_table(values='count', index='hour', aggfunc='sum').reset_index()

def categorize_usage(count):
    if count > 3000:
        return "High Usage"
    elif count > 2000:
        return "Medium Usage"
    else:
        return "Low Usage"

day['Usage Category'] = day['count'].apply(categorize_usage)

st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Pilih data yang ingin ditampilkan:", 
                              ["Top 5 Bike Rentals by Hour","Bike Rentals by Month", "Bike Rentals by Season", 
                               "Bike Rentals Trend (2011 vs 2012)", 
                               "Bike Rentals by Weather", "Usage Category Distribution",
                               ])

st.title("Bike Rentals Dashboard")

if option == "Top 5 Bike Rentals by Hour":
    st.subheader("Top 5 Bike Rentals by Hour")
    top_hours = hour_pivot.nlargest(5, 'count')

    max_value = top_hours['count'].max()
    colors = ['blue' if count == max_value else 'skyblue' for count in top_hours['count']]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax = sns.barplot(x="hour", y="count", data=hour_pivot.nlargest(5, 'count'), 
            palette=["skyblue", "skyblue", "blue", "skyblue", "skyblue"])

    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Total Rentals")
    ax.set_title("Top 5 Bike Rentals by Hour")
    st.pyplot(fig) 

elif option == "Bike Rentals by Month":
    st.subheader("Bike Rentals by Month")
    fig, ax = plt.subplots(figsize=(15, 5))
    max_value = month_pivot['count'].max()
    colors = ['blue' if count == max_value else 'skyblue' for count in month_pivot['count']]
    ax.bar(month_pivot['month'], month_pivot['count'], color=colors)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Rentals")
    st.pyplot(fig)

elif option == "Bike Rentals by Season":
    st.subheader("Bike Rentals by Season")
    fig, ax = plt.subplots(figsize=(8, 5))
    max_value = season_pivot['count'].max()
    colors = ['blue' if count == max_value else 'skyblue' for count in season_pivot['count']]
    ax.bar(season_pivot['season'], season_pivot['count'], color=colors)
    ax.set_xlabel("Season")
    ax.set_ylabel("Total Rentals")
    st.pyplot(fig)

elif option == "Bike Rentals Trend (2011 vs 2012)":
    st.subheader("Bike Rentals Trend by Month (2011 vs 2012)")
    monthly_rentals = day.groupby(['year', 'month'])['count'].sum().unstack(level=0)
    month_labels = ['January','February','March','April','May','June','July','August',
                    'September','October','November','December']
    
    fig, ax = plt.subplots(figsize=(15, 5)) 
    sns.lineplot(x=monthly_rentals.index, y=monthly_rentals[2011], marker='o', label="2011", linewidth=2, color='blue', ax=ax)
    sns.lineplot(x=monthly_rentals.index, y=monthly_rentals[2012], marker='o', label="2012", linewidth=2, color='red', ax=ax)

    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_labels)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Rentals")
    ax.set_title("Bike Rentals Trend by Month (2011 vs 2012)")
    ax.legend()
    st.pyplot(fig)

elif option == "Bike Rentals by Weather":
    st.subheader("Bike Rentals by Weather")
    fig, ax = plt.subplots(figsize=(8, 5))
    max_value = weather_pivot['count'].max()
    colors = ['blue' if count == max_value else 'skyblue' for count in weather_pivot['count']]
    ax.bar(weather_pivot['weather_situation'], weather_pivot['count'], color=colors)
    ax.set_xlabel("Weather")
    ax.set_ylabel("Total Rentals")
    st.pyplot(fig)

elif option == "Usage Category Distribution":
    st.subheader("Usage Category Distribution")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.countplot(x=day['Usage Category'], order=['High Usage', 'Medium Usage', 'Low Usage'], palette='Set1', ax=ax)
    ax.set_xlabel("Usage Category Distribution")
    ax.set_ylabel("Day Totals")
    st.pyplot(fig)


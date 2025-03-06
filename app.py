import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    day = pd.read_csv("clean_day.csv", parse_dates=['dteday'])
    hour = pd.read_csv("clean_hour.csv", parse_dates=['dteday'])
    return day, hour

day, hour = load_data()

# revisi filter data (tanggal)
st.sidebar.title("Filter by Date")
default_start = day['dteday'].min()
default_end = day['dteday'].max()

start_date, end_date = st.sidebar.date_input(
    "Select Date Range:", [default_start, default_end], 
    min_value=default_start, max_value=default_end
)

# date filter
day_filtered = day[(day['dteday'] >= pd.Timestamp(start_date)) & (day['dteday'] <= pd.Timestamp(end_date))]
hour_filtered = hour[(hour['dteday'] >= pd.Timestamp(start_date)) & (hour['dteday'] <= pd.Timestamp(end_date))]

# pivot data setelah filtering
month_pivot = day_filtered.pivot_table(values='count', index='month', aggfunc='sum').reset_index()
season_pivot = day_filtered.pivot_table(values='count', index='season', aggfunc='sum').reset_index()
weather_pivot = day_filtered.pivot_table(values='count', index='weather_situation', aggfunc='sum').reset_index()
hour_pivot = hour_filtered.pivot_table(values='count', index='hour', aggfunc='sum').reset_index()

def categorize_usage(count):
    if count > 3000:
        return "High Usage"
    elif count > 2000:
        return "Medium Usage"
    else:
        return "Low Usage"

day_filtered['Usage Category'] = day_filtered['count'].apply(categorize_usage)

# navigasi
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Pilih data yang ingin ditampilkan (khusus untuk perbandingan tahun mohon filter data dari 2011 sampai 2012:", 
                              ["Rentals by Hour","Bike Rentals by Month", "Bike Rentals by Season", 
                               "Bike Rentals Trend (2011 vs 2012)", 
                               "Bike Rentals by Weather", "Usage Category Distribution",
                               ])

st.title("Bike Rentals Dashboard")

if option == "Rentals by Hour":
    st.subheader("Rentals by Hour")
    top_hours = hour_pivot.nlargest(10, 'count')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="hour", y="count", data=top_hours, color='skyblue')
    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Total Rentals")
    st.pyplot(fig)

elif option == "Bike Rentals by Month":
    st.subheader("Bike Rentals by Month")
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.bar(month_pivot['month'], month_pivot['count'], color='skyblue')
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Rentals")
    st.pyplot(fig)

elif option == "Bike Rentals by Season":
    st.subheader("Bike Rentals by Season")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(season_pivot['season'], season_pivot['count'], color='skyblue')
    ax.set_xlabel("Season")
    ax.set_ylabel("Total Rentals")
    st.pyplot(fig)

elif option == "Bike Rentals Trend (2011 vs 2012)":
    st.subheader("Bike Rentals Trend by Month (2011 vs 2012)")
    monthly_rentals = day_filtered.groupby(['year', 'month'])['count'].sum().unstack(level=0)
    
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.lineplot(x=monthly_rentals.index, y=monthly_rentals[2011], marker='o', label="2011", linewidth=2, color='blue', ax=ax)
    sns.lineplot(x=monthly_rentals.index, y=monthly_rentals[2012], marker='o', label="2012", linewidth=2, color='red', ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Rentals")
    ax.legend()
    st.pyplot(fig)

elif option == "Bike Rentals by Weather":
    st.subheader("Bike Rentals by Weather")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(weather_pivot['weather_situation'], weather_pivot['count'], color='skyblue')
    ax.set_xlabel("Weather")
    ax.set_ylabel("Total Rentals")
    st.pyplot(fig)

elif option == "Usage Category Distribution":
    st.subheader("Usage Category Distribution")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.countplot(x=day_filtered['Usage Category'], order=['High Usage', 'Medium Usage', 'Low Usage'], palette='Set1', ax=ax)
    ax.set_xlabel("Usage Category Distribution")
    ax.set_ylabel("Day Totals")
    st.pyplot(fig)

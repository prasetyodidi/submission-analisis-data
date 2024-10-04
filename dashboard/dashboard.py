import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

sns.set(style='dark')

# Load cleaned data
csv_path = os.path.join(os.path.dirname(__file__), 'main_data.csv')
all_df = pd.read_csv(csv_path)

# Convert 'dteday' to datetime if not already done
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

# Sidebar filters
with st.sidebar:
    # Add company logo
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    # Select two dates for filtering
    start_date = st.date_input("Select Start Date", value=pd.to_datetime('2011-01-01'))
    end_date = st.date_input("Select End Date", value=pd.to_datetime('2012-12-31'))

    # Filter by Season or All (-1 for all seasons)
    all_seasons = [-1, 1, 2, 3, 4]  # 1: Spring, 2: Summer, 3: Fall, 4: Winter
    selected_season = st.selectbox('Select Season (or All Seasons)', all_seasons, format_func=lambda x: 'All' if x == -1 else {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}[x])

# Apply filters to the DataFrame
filtered_df = all_df.copy()

# Filter by selected date range
filtered_df = filtered_df[(filtered_df['dteday'] >= pd.to_datetime(start_date)) & (filtered_df['dteday'] <= pd.to_datetime(end_date))]

# Filter by selected season (if not 'All')
if selected_season != -1:
    filtered_df = filtered_df[filtered_df['season'] == selected_season]

# Group data by hour and calculate total, casual, and registered rentals
hourly_data = filtered_df.groupby('hr').agg({
    'cnt': 'sum',
    'casual': 'sum',
    'registered': 'sum'
}).reset_index()

# Create the plot for hourly rentals
plt.figure(figsize=(10, 6))
sns.lineplot(data=hourly_data, x='hr', y='cnt', label='Total Rentals (cnt)', color='blue')
sns.lineplot(data=hourly_data, x='hr', y='casual', label='Casual Rentals', color='green')
sns.lineplot(data=hourly_data, x='hr', y='registered', label='Registered Rentals', color='red')

# Customize the plot
plt.title('Hourly Bike Rentals (Total, Casual, Registered)')
plt.xlabel('Hour of Day')
plt.ylabel('Rentals')
plt.xticks(range(0, 24))  # Set x-ticks for each hour (0-23)
plt.grid(True)
plt.legend()

# Show the plot in Streamlit
st.pyplot(plt)

# Group by weather situation to calculate total rentals by weather type
weather_rentals = filtered_df.groupby('weathersit')['cnt'].sum().reset_index()

# Map weather situation codes to labels
weather_rentals['weathersit'] = weather_rentals['weathersit'].map({
    1: 'Clear', 
    2: 'Misty', 
    3: 'Light Snow/Rain', 
    4: 'Heavy Rain/Snow'
})

# Sort the data by total rentals in descending order
weather_rentals = weather_rentals.sort_values(by='cnt', ascending=False)

# Create a bar plot for total rentals by weather situation
plt.figure(figsize=(10, 6))
sns.barplot(data=weather_rentals, x='weathersit', y='cnt', palette='viridis')

# Customize the plot
plt.title('Total Bike Rentals by Weather Situation', fontsize=16)
plt.xlabel('Weather Situation', fontsize=14)
plt.ylabel('Total Rentals', fontsize=14)
plt.xticks(rotation=45)

# Show the plot in Streamlit
st.pyplot(plt)

# Display RFM analysis
st.header('RFM Analysis')
rfm_df = pd.DataFrame({
    'User_Type': ['Casual', 'Registered'],  
    'Recency': [10, 5],                     
    'Frequency': [50, 100],                 
    'Monetary': [2000, 5000]                
})

st.write(rfm_df)

plt.figure(figsize=(12, 6))

# Recency
plt.subplot(1, 3, 1)
sns.barplot(x='User_Type', y='Recency', data=rfm_df)
plt.title('Recency by User Type')
plt.ylabel('Average Recency (Days)')

# Frequency
plt.subplot(1, 3, 2)
sns.barplot(x='User_Type', y='Frequency', data=rfm_df)
plt.title('Frequency by User Type')
plt.ylabel('Total Frequency')

# Monetary
plt.subplot(1, 3, 3)
sns.barplot(x='User_Type', y='Monetary', data=rfm_df)
plt.title('Monetary (Total Rentals) by User Type')
plt.ylabel('Total Rentals')

plt.tight_layout()

# Show RFM plots in Streamlit
st.pyplot(plt)

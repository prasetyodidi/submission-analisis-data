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

# Display Manual Grouping and Binning
st.header('Manual Grouping and Binning')

# Define time bins and labels
time_bins = [0, 6, 12, 18, 24]  # Bins for Morning, Afternoon, Evening, Night
time_labels = ['Night (12 AM - 6 AM)', 'Morning (6 AM - 12 PM)', 'Afternoon (12 PM - 6 PM)', 'Evening (6 PM - 12 AM)']

# Create a new column 'time_of_day' based on 'hr'
filtered_df['time_of_day'] = pd.cut(filtered_df['hr'], bins=time_bins, labels=time_labels, right=False)

# Group by 'time_of_day' and calculate the mean of 'casual' and 'registered' rentals
grouped_data = filtered_df.groupby('time_of_day')[['casual', 'registered']].mean().reset_index()

# Output the result
print(grouped_data)

# Plot casual and registered users by time of day
grouped_data.set_index('time_of_day').plot(kind='bar', figsize=(10, 6), stacked=False)
plt.title('Average Casual vs Registered Users by Time of Day')
plt.ylabel('Average Number of Users')
plt.xlabel('Time of Day')
plt.xticks(rotation=45)
plt.show()

st.pyplot(plt)

# Define temperature bins and labels (normalized temperature divided by max 41°C)
temp_bins = [0.0, 0.3, 0.6, 0.9, 1.0]  # Corresponding to Cold, Moderate, Warm, Hot
temp_labels = ['Cold (0°C - 12.3°C)', 'Moderate (12.3°C - 24.6°C)', 'Warm (24.6°C - 36.9°C)', 'Hot (36.9°C - 41°C)']

# Create a new column 'temp_range' based on 'temp' bins
filtered_df['temp_range'] = pd.cut(filtered_df['temp'], bins=temp_bins, labels=temp_labels, right=False)

# Group by 'temp_range' and calculate the mean of 'cnt' (total bike rentals)
grouped_data = filtered_df.groupby('temp_range')['cnt'].mean().reset_index()

# Output the result
print(grouped_data)

# Plot the results using matplotlib for visual representation
plt.figure(figsize=(10, 6))
plt.bar(grouped_data['temp_range'], grouped_data['cnt'], color='skyblue')
plt.title('Average Bike Rentals by Temperature Range')
plt.ylabel('Average Total Rentals (cnt)')
plt.xlabel('Temperature Range')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

st.pyplot(plt)


# Define season labels
season_labels = ['Spring', 'Summer', 'Fall', 'Winter']

# Create a new column 'season_label' based on 'season' values
filtered_df['season_label'] = filtered_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

# Group by 'season_label' and calculate the mean of 'casual' and 'registered' rentals
grouped_data = filtered_df.groupby('season_label')[['casual', 'registered']].mean().reset_index()

# Output the result
print(grouped_data)

# Plot the results using matplotlib for visual representation
grouped_data.set_index('season_label').plot(kind='bar', figsize=(10, 6), stacked=False, color=['skyblue', 'orange'])
plt.title('Average Casual vs Registered Users by Season (Hourly Data)')
plt.ylabel('Average Number of Users')
plt.xlabel('Season')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

st.pyplot(plt)



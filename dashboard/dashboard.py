import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import os

sns.set(style='dark')

# Load cleaned data
csv_path = os.path.join(os.path.dirname(__file__), 'main_data.csv')
all_df = pd.read_csv(csv_path)

# Convert 'dteday' to datetime if not already done
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

# Get min/max dates for the date filter
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

# Sidebar filters
with st.sidebar:
    # Add company logo
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    all_years = [-1] + sorted(all_df['yr'].unique().tolist())
    selected_year = st.selectbox('Select Year (or All Years)', all_years, format_func=lambda x: 'All' if x == -1 else f"201{str(x+1)}")

    # Filter by Season or All (-1 for all seasons)
    all_seasons = [-1, 1, 2, 3, 4]  # 1: Spring, 2: Summer, 3: Fall, 4: Winter
    selected_season = st.selectbox('Select Season (or All Seasons)', all_seasons, format_func=lambda x: 'All' if x == -1 else {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}[x])

    # Filter by Weather Situation or All (-1 for all weather situations)
    all_weather = [-1, 1, 2, 3, 4]  # 1: Clear, 2: Misty, 3: Light Snow/Rain, 4: Heavy Rain/Snow
    selected_weather = st.selectbox('Select Weather Situation (or All)', all_weather, format_func=lambda x: 'All' if x == -1 else {1: 'Clear', 2: 'Misty', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'}[x])

# Apply filters to the DataFrame
filtered_df = all_df.copy()

# Filter by selected year (if not 'All')
if selected_year != -1:
    filtered_df = filtered_df[filtered_df['yr'] == selected_year]

# Filter by selected season (if not 'All')
if selected_season != -1:
    filtered_df = filtered_df[filtered_df['season'] == selected_season]

# Filter by selected weather situation (if not 'All')
if selected_weather != -1:
    filtered_df = filtered_df[filtered_df['weathersit'] == selected_weather]

# Now filtered_df contains the data according to the selected filters.
st.write(filtered_df)



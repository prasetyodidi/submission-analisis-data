# Bike Sharing Dataset Dashboard

## Overview
This project focuses on exploring and visualizing data from the **Bike Sharing Dataset**. It leverages Streamlit to create interactive visualizations that provide insights into the factors affecting bike rentals, such as weather conditions, seasonality, and user types. The goal is to analyze the dataset comprehensively, highlighting trends, patterns, and key metrics within the bike-sharing landscape.

## Data Source
The data used in this project comes from the following source:

- [Bike Sharing Dataset](https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset)

## Requirements
To run this project, you need to install the following Python packages:

- Babel==2.11.0
- matplotlib==3.8.4
- numpy==1.26.4
- pandas==2.2.2
- seaborn==0.13.2
- streamlit==1.32.0

You can find the required packages listed in the `requirements.txt` file.

## Installation

### Clone the Repository
First, clone the repository:

```bash
git clone https://github.com/prasetyodidi/submission-analisis-data.git
cd submission-analisis-data
```


## Create a virtual environment

```
python -m venv venv
```

## Activate the virtual environment
### On Windows
```
venv\Scripts\activate
```
### On macOS/Linux
```
source venv/bin/activate
```

## Install Dependencies
### Install the required packages:

```
pip install -r requirements.txt
```

## Prepare Data

Ensure that you have the following CSV files in the `data` directory:

- `day.csv`: Contains daily records of bike rentals.
- `hour.csv`: Contains hourly records of bike rentals.

### Dataset Fields:
**Common Fields (in both `hour.csv` and `day.csv`, except `hr`):**

- `instant`: Record index.
- `dteday`: Date.
- `season`: Season (1: Spring, 2: Summer, 3: Fall, 4: Winter).
- `yr`: Year (0: 2011, 1: 2012).
- `mnth`: Month (1 to 12).
- `holiday`: Whether the day is a holiday (based on DC holiday schedule).
- `weekday`: Day of the week.
- `workingday`: Whether the day is a working day (1 for working days, 0 for weekends/holidays).
- `weathersit`: Weather situation (1: Clear, 2: Misty, 3: Light Snow/Rain, 4: Heavy Rain/Snow).
- `temp`: Normalized temperature.
- `atemp`: Normalized feeling temperature.
- `hum`: Normalized humidity.
- `windspeed`: Normalized wind speed.
- `casual`: Count of casual users (non-registered).
- `registered`: Count of registered users.
- `cnt`: Total bike rentals (sum of casual and registered).

**Hour-Specific Field (in `hour.csv` only):**

- `hr`: Hour of the day (0 to 23).

Make sure these files are correctly placed in the data directory or adjust the file paths in `dashboard.py` if necessary.

## Running the Dashboard
### Run the Streamlit application:

streamlit run dashboard/dashboard.py

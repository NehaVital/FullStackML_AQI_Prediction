import requests
import csv
from datetime import datetime
import pandas as pd

# Correct API endpoint for AQI data
API_ENDPOINT = 'https://api.weatherbit.io/v2.0/history/airquality?lat=17.4237&lon=78.4584&city=Hyderabad%20India&postal_code=500082&country=In&key=15cadf07775b46e8898bef8905d6114c'

def fetch_aqi_data(API_ENDPOINT):
    params = {
        'lat': 17.4237,
        'lon': 78.4584,
        'city_id': '',
        'city': 'Hyderabad,India',
        'postal_code': 500082,
        'country': 'In',
        'key': '15cadf07775b46e8898bef8905d6114c'
    }
    response = requests.get(API_ENDPOINT, params=params)

    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def append_to_csv(aqi_data, csv_file):
    if aqi_data:
        # Check if the CSV file already exists
        try:
            existing_data = pd.read_csv(csv_file)
        except FileNotFoundError:
            existing_data = pd.DataFrame()

        # Append the new AQI data to the existing data
        new_data = []
        for entry in aqi_data:
            aqi_value = entry.get('aqi')
            date = entry.get('timestamp_local')[0:10]
            time = entry.get('timestamp_local')[11:16]
            local_time = date.split(' ')
            new_data.append([aqi_value, date, time])

        final_data = pd.concat([existing_data, pd.DataFrame(new_data, columns=['AQI', 'Date', 'Time'])], ignore_index=True)

        # Save the combined data to the CSV file
        final_data.to_csv(csv_file, index=False)

        print(f"Data appended to CSV file '{csv_file}' successfully.")
    else:
        print("No data to append to CSV.")

aqi_data = fetch_aqi_data(API_ENDPOINT)
if aqi_data:
    csv_file = 'aqi_data.csv'
    append_to_csv(aqi_data, csv_file)

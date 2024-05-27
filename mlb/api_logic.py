import requests
import os 
import json
from dotenv import load_dotenv

def load_data(DATE, PATH, ENDPOINT ):
    '''If PATH exists, open it and return data.
    Else call api ENDPOINT to get specific DATE data and then save it locally
    
    Return: (dict) json response from api
    '''
    data = None
    try:
        if os.path.isfile(PATH):
            print(f"Loading data from cache: {PATH}")
            with open(PATH, 'r') as file:
                data = json.load(file)
        else:
            print(f"Calling API for new data: {DATE}")
            data = _call_api(DATE,ENDPOINT)
            _save_data_locally(data, PATH)
    except Exception as e:
        print(f"Error loading data: {e}")
    return data

def full_path_schedules(date):
    """With given date, constructs and returns the (string)path for the cache_schedules directory + filename"""
    filename = f"daily_schedule_{date}"
    dir_path = os.path.join("mlb", "cache_schedules")
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, filename)

def _call_api(date, url):
    """Calls the Tank MLB API to return the (dict)for a given date and endpoint."""
    query_string = {"gameDate": date}
    load_dotenv()
    headers = {
        "X-RapidAPI-Key": os.getenv('API_KEY'),
        "X-RapidAPI-Host": os.getenv('HOST')
    }
    response = requests.get(url, headers=headers, params=query_string)
    return response.json()

def _save_data_locally(data, full_path):
    """Saves the given data to a local json file at the specified path."""
    try:
        with open(full_path, 'w') as file:
            json.dump(data, file)
    except Exception as e:
        print(f"Error saving data locally: {e}")


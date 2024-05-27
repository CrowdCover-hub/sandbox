import mlb_teams
import requests
import os 
import json
from dotenv import load_dotenv


def get_daily_schedule(date):
    """
    Retrieves and returns a sorted list of MLB games for a specific date. Could generate API call.

    Parameters:
    date (str): The date for which to get the schedule, in 'YYYYMMDD' format.
    """
    data = _load_schedule_data(date)
    sorted_data = _sort_games(data)
    return sorted_data

def get_timetable(sorted_games):
    """
    Constructs and returns a (dict)timetable of games.

    Parameters:
    sorted_games (list): A list provided by 'get_daily_schedule(date)'. 
    """
    game_timetable = {}
    for game_ID in sorted_games:
        game_data = {
            'away': mlb_teams.get_team(game_ID['away']),
            'home': mlb_teams.get_team(game_ID['home']),
            'game_time': game_ID['gameTime'],
            'game_date': game_ID['gameDate'],
        }
        game_timetable[game_ID['gameID']] = game_data
    return game_timetable

#---- [Private functions] ----#

def _load_schedule_data(date):
    '''If schedule file for date exists, open it from provided full_path.
    Else call api to get schedule data and save it locally'''
    data = None
    full_path = _get_full_path(date)
    try:
        if os.path.isfile(full_path):
            print(f"Loading data from cache: {full_path}")
            with open(full_path, 'r') as file:
                data = json.load(file)
        else:
            print(f"Calling API for new schedule data: {date}")
            data = _call_api_schedules(date)
            _save_data_locally(data, full_path)
    except Exception as e:
        print(f"Error loading data: {e}")
    return data

def _get_full_path(date):
    """Constructs and returns the (string)path for the cache_schedules directory + filename with date"""
    filename = f"daily_schedule_{date}"
    dir_path = os.path.join("mlb", "cache_schedules")
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, filename)

def _call_api_schedules(date):
    """Calls the Tank MLB API to return the (dict)daily-schedule for a given date."""
    query_string = {"gameDate": date}
    load_dotenv()
    headers = {
        "X-RapidAPI-Key": os.getenv('API_KEY'),
        "X-RapidAPI-Host": os.getenv('HOST')
    }
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBGamesForDate"
    response = requests.get(url, headers=headers, params=query_string)
    return response.json()

def _save_data_locally(data, full_path):
    """Saves the given data to a local file at the specified path."""
    try:
        with open(full_path, 'w') as file:
            json.dump(data, file)
    except Exception as e:
        print(f"Error saving data locally: {e}")

def _sort_games(data):
    """Sorts the given data by game time and returns the (list)sorted data."""
    if not isinstance(data, dict):
        raise ValueError("Invalid data: must be a dictionary")
    games = data.get('body', [])
    return sorted(games, key=lambda game: float(game['gameTime_epoch']))


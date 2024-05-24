import mlb_teams
import requests
import os 
import json
from dotenv import load_dotenv


def get_daily_schedule(date):
     """
     Returns sorted list of MLB games scheduled for a specific date
     'date' format: YYYYMMDD
     """
     # Step 1: Check if file already exists in local cache
     filename = f"daily_schedule_{date}"
     full_path = _helper_fullpath(filename)
     file_exists = os.path.isfile(full_path)
     
     # Step 2: If no file exists, call API to create data.
     #         Else load data with cached file
     data = None
     if (not file_exists): 
          data = _call_api(date)
          _save_data_locally(data)
     else: 
          # TODO: make this a helper function
          with open(full_path, 'r') as file:
               data = json.load(file) 
               print(f"Data loaded from file: {full_path}")
               
     # Step 3: Sort and return games
     data =_sort_games(data)
     return data
#---------------------------------------------------------------------------------------------------------------------
def _call_api(date):
     '''Calls Tank MLB api to get daily schedule'''
     # Step 1: build http request
     query_string = {"gameDate":date}
     load_dotenv()
     headers = {
          "X-RapidAPI-Key": os.getenv('API_KEY'),
          "X-RapidAPI-Host": os.getenv('HOST')
     }
     
     # Step 2: try to call API & return data
     try:
          url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBGamesForDate"
          print(f"Calling API: {url}")
          response = requests.get(url, headers=headers, params=query_string)
          data = response.json()
     except Exception as e:
          print(f"- Error: {e}")
          print(f"- Response: {response}")
     return data
#---------------------------------------------------------------------------------------------------------------------
def _sort_games(data):
     """Sorts the raw Tank MLB json (daily_schedules) by their starting game time"""
     if not isinstance(data, dict):
          print("Invalid data: must be a dictionary")
          return
     
     #Get & sort raw json body payload
     games = data.get('body', [])
     sorted_games = sorted(games, key=lambda game: float(game['gameTime_epoch']))
     return sorted_games

#---------------------------------------------------------------------------------------------------------------------
def print_sorted_games(sorted_games):
     '''Takes return "data" from  "get_daily_schedule(date)"'''
     count = 0
     for game in sorted_games:
          count += 1
          print(f"\n------------Game {count}------------")
          print(f"Game ID: {game['gameID']}")
          print(f"Game Type: {game['gameType']}")
          print(f"Away Team: {game['away']}")
          print(f"Game Time: {game['gameTime']}")# Game Time is always in Eastern time zone
          print(f"Game Date: {game['gameDate']}")
          print(f"Home Team ID: {game['teamIDHome']}")
          print(f"Game Time Epoch: {game['gameTime_epoch']}")
          print(f"Away Team ID: {game['teamIDAway']}")
          print(f"Probable Starting Pitchers: {game['probableStartingPitchers']}")
          print(f"Home Team: {game['home']}")
#---------------------------------------------------------------------------------------------------------------------
def get_timetable(sorted_games):
     '''Return a nested dictionary from get_daily_schedule'''
     frontend_data = {} # This is a nested dictionary
     
     # Iterate over the sorted games
     for game in sorted_games:
          # Create a nested dictionary for each game
          dict_entry = {
               'away': mlb_teams.get_team(game['away']),
               'home': mlb_teams.get_team(game['home']),
               'gameTime': game['gameTime'],# Game Time is always in Eastern time zone
               'gameDate': game['gameDate'],   
          }

          # Add the nested dictionary to the frontend_data dictionary
          frontend_data[game['gameID']] = dict_entry
     return frontend_data
#---------------------------------------------------------------------------------------------------------------------
def _save_data_locally(data,fullpath):
     try:
          with open(fullpath, 'w') as file:
               json.dump(data, file)
               print(f"New file created: {fullpath}")
     except Exception as e:
          print(f"Error saving data locally: {e}")
               
def _helper_fullpath(filename):
     '''Calculates directory path for caching schedules'''
     # Create the directory if it doesn't exist
     dir_path = os.path.join("mlb", "cache_schedules")
     os.makedirs(dir_path, exist_ok=True)
     
     # Calculate and return full_path
     full_path = os.path.join(dir_path, filename)
     return full_path
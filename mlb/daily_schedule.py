import mlb_teams
import requests
import os 
import json
from dotenv import load_dotenv


def get_daily_schedule(date):
     """
     Automatically gets daily schedules
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
          data = _call_api(date, full_path)
     else: 
          # TODO: make this a helper function
          with open(full_path, 'r') as file:
               data = json.load(file) 
               print(f"Data loaded from file: {full_path}")
               
     # Step 3: Sort and return games
     data =_sort_games(data)
     return data
#---------------------------------------------------------------------------------------------------------------------
def _call_api(date,filename):
     '''Calls Tank MLB api to get daily schedule'''
     # Step 1: build http request
     query_string = {"gameDate":date}
     load_dotenv()
     headers = {
          "X-RapidAPI-Key": os.getenv('API_KEY'),
          "X-RapidAPI-Host": os.getenv('HOST')
     }
     
     # Step 2: try to call API
     try:
          url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBGamesForDate"
          print(f"Calling API: {url}")
          response = requests.get(url, headers=headers, params=query_string)
          data = response.json()
          with open(filename, 'w') as f:
               json.dump(data, f)
               print(f"New file created: {filename}")
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
def _get_post_body(sorted_games):
     # TODO: build the json package to be delivered to frontend WordPress Rest API
     return
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
def _build_json_body(sorted_games):
     frontend_data = {}
     
     # Iterate over the sorted games
     for game in sorted_games:
          
          # Create a nested dictionary for each game
          nested_dict = {
               'away': mlb_teams.get_team(game['away']),
               'home': mlb_teams.get_team(game['home']),
               'gameTime': game['gameTime'],# Game Time is always in Eastern time zone
               'gameDate': game['gameDate'],   
          }

          # Add the nested dictionary to the frontend_data dictionary
          frontend_data[game['gameID']] = nested_dict
     return frontend_data
#---------------------------------------------------------------------------------------------------------------------
def save_json_locally(data,filename, dir_path):
     # TODO: add try, except
     with open(filename, 'w') as f:
               json.dump(data, f)
               print(f"New file created: {filename}")
               
def _helper_fullpath(filename):
     '''Calculates directory path for caching schedules'''
     # Create the directory if it doesn't exist
     dir_path = os.path.join("mlb", "cache_schedules")
     os.makedirs(dir_path, exist_ok=True)
     
     # Calculate and return full_path
     full_path = os.path.join(dir_path, filename)
     return full_path
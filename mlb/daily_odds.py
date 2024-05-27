import requests
import os 
import json
from dotenv import load_dotenv

def get_team_odds(date):
     '''get all MLB Betting Odds from a date'''
     _call_api_odds(date)
     return

def _call_api_odds(date):
     '''Calls Tank MLB api to get provided 'date'(YYYYMMDD) odds'''
     query_string = {"gameDate": date}
     load_dotenv()
     headers = {
          "X-RapidAPI-Key": os.getenv('API_KEY'),
          "X-RapidAPI-Host": os.getenv('HOST')
     }
     url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBettingOdds"
     response = requests.get(url, headers=headers, params=query_string)
     print(response.json())
     return response.json()
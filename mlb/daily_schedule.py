import mlb_teams
import api_logic

def get_daily_schedule(DATE):
    """
    Retrieves and returns a sorted list of MLB games for a specific date. Could generate API call.

    Parameters:
    DATE (str): The date for which to get the schedule, in 'YYYYMMDD' format.
    """
    #prepare API call and cache location
    ENDPOINT = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBGamesForDate"
    PATH = api_logic.full_path_schedules(DATE)

    #load data from either cache PATH or api ENDPOINT
    DATA = api_logic.load_data(DATE, PATH, ENDPOINT)

    #return sorted game schedule data
    return _sort_games(DATA)

def get_timetable(SORTED_GAMES):
    """
    Constructs and returns a (dict)timetable of games.

    Parameters:
    sorted_games (list): A list provided by 'get_daily_schedule(date)'. 
    """
    game_timetable = {}
    for game_ID in SORTED_GAMES:
        game_data = {
            'away': mlb_teams.get_team(game_ID['away']),
            'home': mlb_teams.get_team(game_ID['home']),
            'game_time': game_ID['gameTime'],
            'game_date': game_ID['gameDate'],
        }
        game_timetable[game_ID['gameID']] = game_data
    return game_timetable

#---- [Private functions] ----#

def _sort_games(data):
    """Sorts the given game data by game time and returns the (list)sorted data."""
    if not isinstance(data, dict):
        raise ValueError("Invalid data: must be a dictionary")
    games = data.get('body', [])
    return sorted(games, key=lambda game: float(game['gameTime_epoch']))
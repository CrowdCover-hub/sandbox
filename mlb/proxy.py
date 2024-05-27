import daily_schedule

class MLB_logic:
     _instance = None
     date = None
     timetable = None
          
     def execute(self):
          '''Sets date for MLB logic and executes logic'''
          self.date = 20240522 # temporary
          # self.date = input("Enter the desired MLB day (YYYYMMDD): ")
          print(f"Chosen date is {self.date}")

          self._update_timetable()

     def print_daily_data(self):
          print("Today's timetable is:")
          # Iterate over each game in the timetable and print its start time
          for game_ID in self.timetable:
               game = self.timetable[game_ID]
               print(f"\n---- Game ID: {game_ID} ----")
               print(f"{game['away']} vs {game['home']} at '{game['game_time']}'")
     
     #---- [Private functions] ----#

     def _update_timetable(self):
          '''Update data to the given day'''
          schedule = daily_schedule.get_daily_schedule(self.date)
          self.timetable = daily_schedule.get_timetable(schedule)
          

     def _get_team_odds():
          return
     
     def __new__(cls, *args, **kwargs):
          '''Ensures singleton pattern'''
          if not cls._instance:
               cls._instance = super(MLB_logic, cls).__new__(cls, *args, **kwargs)
          return cls._instance
     

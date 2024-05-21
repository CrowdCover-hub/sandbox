import daily_schedule


def main():
     # Get user input
     date = input("Enter the desired MLB daily schedule date (YYYYMMDD): ")
     post_daily_schedule(int(date))

def post_daily_schedule(date):
     #Get games from API
     print("Getting daily schedule.")
     data = schedule_data = daily_schedule.get_daily_schedule(date)
     #print game schedule data
     daily_schedule.print_sorted_games(data)
     return 0

#------------------------------ Execute 
if __name__ == "__main__":
     main()
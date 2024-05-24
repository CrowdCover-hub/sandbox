import daily_schedule

def MLB_process():
     date = 20240522
     # date = input("Enter the desired MLB daily schedule date (YYYYMMDD): ")
     print(f"Chosen date is {date}")
     timetable = daily_schedule.get_timetable(daily_schedule.get_daily_schedule(date))
     
     print(type(timetable))
     for item in timetable:
          print(item)
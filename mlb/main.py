import proxy

def main():
     ''''''
     print("----Start of Program----")
     mlb=proxy.MLB_logic()
     mlb.execute()
     mlb.print_daily_data()
     print("----End of Program----")
     return 0

#------------------------------ Execute 
if __name__ == "__main__":
     main()
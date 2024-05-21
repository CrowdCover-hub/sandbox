team_ID = {
     "ARI" : "Arizona Diamondbacks",#
     "ATL" : "Atlanta Braves",#
     "BOS" : "Boston Red Sox",#
     "CHC" : "Chicago Cubs",#
     "CHW" : "Chicago White Sox",#
     "CIN" : "Cincinnati Reds",#
     "CLE" : "Cleveland Guardians",#
     "COL" : "Colorado Rockies",#
     "DET" : "Detroit Tigers",#
     "FLA" : "Florida Marlins",
     "HOU" : "Houston Astros",#
     "KCR" : "Kansas City Royals",
     "KC"  : "Kansas City Royals",#
     "LAA" : "Los Angeles Angels",#
     "LAD" : "Los Angeles Dodgers",#
     "MIA" : "Miami Marlins",#
     "MIL" : "Milwaukee Brewers",#
     "MIN" : "Minnesota Twins",#
     "NYM" : "New York Mets",#
     "NYY" : "New York Yankees",#
     "OAK" : "Oakland Athletics",#
     "PHI" : "Philadelphia Phillies",#
     "PIT" : "Pittsburgh Pirates",#
     "SDP" : "San Diego Padres",
     "SD"  : "San Diego Padres",#
     "SFG" : "San Francisco Giants",
     "SF"  : "San Francisco Giants",
     "SEA" : "Seattle Mariners",#
     "STL" : "St. Louis Cardinals",#
     "TBR" : "Tampa Bay Rays",#
     "TB"  : "Tampa Bay Rays",
     "TEX" : "Texas Rangers",#
     "TOR" : "Toronto Blue Jays",#
     "WSN" : "Washington Nationals",
     "WAS" : "Washington Nationals",#
     "BAL" : "Baltimore Orioles"#
}

def get_team(team_code):
     return team_ID.get(team_code)

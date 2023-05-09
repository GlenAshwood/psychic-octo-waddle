from csv import reader,DictReader
from prettytable import PrettyTable
import os

def ingest_file(file_name):
    home_win,away_win,draw,goals = 0,0,0,0
    team_results = []
    with open(file_name) as results:
        csv_reader = DictReader(results)
        for row in csv_reader:
            #call get_score function
            x = get_score(row)
            #call get_result function 
            result= get_result(x)
            #save team names
            home_team, away_team = row["Home Team"],row["Away Team"]
            
            #call update_team and returns stats in a dict
            home_details = (update_team(home_team, "home", result, x[0], x[1]))
            away_details = (update_team(away_team, "away", result, x[1], x[0]))

            #check if first game
            hidx = search(home_team, team_results)
            aidx = search(away_team, team_results)

            #update team_results
            if hidx == None:
                team_results.append(home_details)
            else:
                home_update = update_history(team_results[hidx], home_details)

            if aidx == None:
                team_results.append(away_details)
            else:
                away_update = update_history(team_results[aidx], away_details)
    
    team_results = sorted(team_results, key = lambda i: (i['points'], i['GD']), reverse=True)

    print_table(team_results)    

#prints the result in a table
def print_table(final):
    x = PrettyTable(["Club", "MP", "W", "D", "L", "GF", "GA", "GD", "Pts",]) 
    x.align["Club"] = "l" # Left align city names 
    x.padding_width = 1 # One space between column edges and contents (default) 
    for team in final:
        x.add_row([team["team"], team["MP"], team["W"], team["D"], team["L"],
                        team["GF"], team["GA"], team["GD"], team["points"]])
    os.system('clear')
    print(x)

#returns the list index if entry exists 
def search(team, l):
    idx = 0
    for t in l:
        if t["team"] == team:
            return idx
        idx += 1
    return None

# adds current stats to historic stats and returns the result
def update_history(history, new):
    result = history
    result["MP"] += 1
    result["W"] += new["W"]
    result["D"] += new["D"]
    result["L"] += new["L"]
    result["GF"] += new["GF"]
    result["GA"] += new["GA"]
    result["GD"] += new["GD"]
    result["points"] += new["points"]
    return result

#Splits the score and returns as a list
def get_score(row):
    x = row["Result"].split(" - ")
    x[0] = int(x[0])
    x[1] = int(x[1])
    return x

#returns result and splits the 
def get_result(x):
    if x[0] > x[1]:
        return "home"
    elif x[0] < x[1]:
        return "away"
    else:
        return "draw"

# calc the points and GD and returns as a dict
def update_team(team_name, loc, result, GF, GA):
    team_details = {"team": team_name, "MP": 1, "W": 0, "D": 0, "L": 0, "GF": GF, "GA": GA,"GD": 0, "points": 0}
    if loc == result:
        team_details["points"] = 3
        team_details["W"] = 1
    elif result == "draw":
        team_details["points"] = 1
        team_details["D"] = 1
    else:
        team_details["L"] = 1
    team_details["GD"] = GF - GA
    return team_details


#########
#### Call function - run program
ingest_file("epl-2017-GMTStandardTime.csv")
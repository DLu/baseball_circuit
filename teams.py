import csv

TEAMS = None

def get_team_data():
    global TEAMS
    if TEAMS:
        return TEAMS
    TEAMS = {}
        
    for x in csv.DictReader(open('teams.csv'), delimiter='\t'):
        TEAMS[ x['TLA'] ] = x
    return TEAMS    


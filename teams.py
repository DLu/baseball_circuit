import csv

TEAMS = None

def get_team_data():
    global TEAMS
    if TEAMS:
        return TEAMS
    TEAMS = {}

    for x in csv.DictReader(open('teams.csv'), delimiter='\t'):
        x['MLB_NUM'] = int(x['MLB_NUM'])
        TEAMS[x['TLA']] = x

    return TEAMS

def all_teams():
    teams = get_team_data()
    return sorted(teams.keys())

def lookup_by_name(name):
    teams = get_team_data()

    for tla in teams:
        if teams[tla]['Name'] == name:
            return tla
    return None

def get_mlb_num(tla):
    return get_team_data()[tla]['MLB_NUM']

def get_team_name(tla):
    return get_team_data()[tla]['Name']

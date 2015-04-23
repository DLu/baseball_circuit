#!/usr/bin/python

from datetime import datetime, timedelta
import calendar
import urllib2

YEAR = 2013

NAMES = {'D-backs': 'ARI', 'Braves': 'ATL', 'Orioles': 'BAL', 'Red Sox': 'BOS', 'Cubs': 'CHC', 'Reds': 'CIN', 'Indians': 'CLE', 'Rockies': 'COL', 'White Sox': 'CWS', 'Tigers': 'DET', 'Astros': 'HOU', 'Royals': 'KC', 'Dodgers': 'LA', 'Angels': 'LAA', 'Marlins': 'MIA', 'Brewers': 'MIL', 'Twins': 'MIN', 'Mets': 'NYM', 'Yankees': 'NYY', 'Athletics': 'OAK', 'Phillies': 'PHI', 'Pirates': 'PIT', 'Padres': 'SD', 'Mariners': 'SEA', 'Giants': 'SF', 'Cardinals': 'STL', 'Rays': 'TB', 'Rangers': 'TEX', 'Blue Jays': 'TOR', 'Nationals': 'WAS'}

def read_schedule(csv):
    header = None
    games = []
    for line in csv.split('\n'):
        row = line.split(',')
        if header is None:
            header = row
        else:
            (date, time, teams) = (row[0], row[2], row[3])
            i = teams.index(' at ')
            if 'All-Stars' in teams:
                continue
            away = NAMES[teams[:i].strip()]
            home = NAMES[teams[i+3:].strip()]
            if time == '03:33 AM':
                hour = 19
                mins = 0
            else:
                hour = int(time[:2])
                mins = int(time[3:5])
            if 'PM' in time and hour!=12:
                hour += 12
            t = datetime(YEAR, int(date[:2]), int(date[3:5]), hour, mins)
            stamp = calendar.timegm(t.utctimetuple())
            games.append( (stamp, away, home) )
    return games


schedule = []

for num in [109, 144, 110, 111, 112, 113, 114, 115, 145, 116, 117, 118, 119, 108, 146, 158, 142, 121, 147, 133, 143, 134, 135, 136, 137, 138, 139, 140, 141, 120]:
    response = urllib2.urlopen('http://mlb.mlb.com/soa/ical/schedule.csv?home_team_id=%d&season=%d'%(num, YEAR))
    schedule += read_schedule(response.read())

for x in sorted(schedule):
    print '%d\t%s\t%s'%x

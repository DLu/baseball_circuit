#!/usr/bin/python

from datetime import datetime, timedelta
import calendar
import urllib2
import csv
from teams import *

YEAR = 2015

def get_datetime(date, time):
    if time == '03:33 AM':
        hour = 19
        mins = 0
    else:
        hour = int(time[:2])
        mins = int(time[3:5])
    if 'PM' in time and hour!=12:
        hour += 12
    t = datetime(YEAR, int(date[:2]), int(date[3:5]), hour, mins)
    return calendar.timegm(t.utctimetuple())

def read_schedule(file_obj, remove_spring=True):
    games = []
    venues = []
    
    for data in csv.DictReader(file_obj, delimiter=','):
        date = data['START_DATE']
        time = data['START_TIME_ET']
        teams = data['SUBJECT']
        
        if 'All-Stars' in teams:
            continue

        away_name, _, home_name = teams.partition(' at ')
        away = lookup_by_name(away_name)
        home = lookup_by_name(home_name)
        
        if away is None or home is None:
            print 'Skipping %s @ %s (%s)'%(away_name, home_name, date)
            continue
            
        stamp = get_datetime(date, time)    
        
        games.append( (stamp, away, home) )
        venues.append( data['LOCATION'] )
        
    if remove_spring:
        season = []
        final = venues[-1]
        for game, stadium in zip(games, venues):
            if stadium == final:
                season.append(game)
        games = season        
        
    return games

def get_filename(number, year):
    return 'http://mlb.mlb.com/soa/ical/schedule.csv?home_team_id=%d&season=%d'%(number, year)

def get_games(number, year):
    response = urllib2.urlopen( get_filename(number, year) )
    return read_schedule(response)

if __name__=='__main__':
    import argparse    
    parser = argparse.ArgumentParser(description='Schedule Downloader')
    parser.add_argument('year', type=int)
    parser.add_argument('teams', metavar='team', nargs='*')
    args = parser.parse_args()
    if len(args.teams)==0:
        args.teams = all_teams()
    
    for team in args.teams:
        print get_games( get_mlb_num(team), args.year )

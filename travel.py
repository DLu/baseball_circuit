import collections
import csv

DISTANCES = None
TIMES = None

def read_distance_data():
    global DISTANCES, TIMES
    DISTANCES = collections.defaultdict(dict)
    TIMES = collections.defaultdict(dict)
    
    for x in csv.DictReader(open('distances.csv'), delimiter='\t'):
        t1 = x['TEAM1']
        t2 = x['TEAM2']
        
        DISTANCES[t1][t2] = int(x['DistanceInMeters'])
        DISTANCES[t2][t1] = DISTANCES[t1][t2]
        TIMES[t1][t2] = int(x['TimeInSeconds'])
        TIMES[t2][t1] = TIMES[t1][t2]

def get_distance_data():
    global DISTANCES
    if DISTANCES:
        return DISTANCES
    read_distance_data()
    return DISTANCES

def get_time_data():
    global TIMES
    if TIMES:
        return TIMES
    read_distance_data()
    return TIMES


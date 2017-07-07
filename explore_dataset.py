from functools import partial
import pandas as pd
from datetime import datetime
from pandas import DataFrame


_DRAW_ = 'draw'
_HOME_WIN_ = 'home'
_AWAY_WIN_ = 'away'

_STATS_COLUMNS_ = ['shoton', 'shotoff', 'cross', 'foulcommit', 'corner']
_DELETE_COLUMNS_ = ['shoton', 'shotoff', 'cross',
                    'foulcommit', 'corner', 'id',
                    'stage', 'date', 'match_api_id', 'home_team_api_id']

def calculate_label(match):
    if match['home_team_goal'] == match['away_team_goal']:
        return _DRAW_
    elif match['home_team_goal'] > match['away_team_goal']:
        return _HOME_WIN_
    else:
        return _AWAY_WIN_


def calculate_stat(team_id, stat_name, match):
    return str(match[stat_name]).count(str(team_id))


def calculate_stat_home(stat_name, match):
    team_id = match['home_team_api_id']
    return str(match[stat_name]).count(str(team_id))


def calculate_stat_away(stat_name, match):
    team_id = match['away_team_api_id']
    return str(match[stat_name]).count(str(team_id))


def extract_stats_by_team_id(data, team_id):
    matches_home = extract_matches_by_home_team(data, team_id)
    matches_away = extract_matches_by_away_team(data, team_id)
    stats = matches_home.append(matches_away)
    stats = add_time_index(stats)
    return stats


def add_time_index(df):
    df['date'] = pd.to_datetime(df['date'])
    df.index = df['date']
    del df['date']
    return df


def extract_matches_by_home_team(data, team_id):
    match_by_team = data[(data['home_team_api_id'] == team_id)]
    stats = match_by_team[
        ['home_team_api_id', 'date', 'home_shoton', 'home_shotoff', 'home_cross', 'home_foulcommit', 'home_corner']]
    return stats.rename(columns=lambda col: col.replace('home_', ""))

def extract_matches_by_away_team(data, team_id  ):
    match_by_team = data[(data['away_team_api_id'] == team_id)]
    stats = match_by_team[
        ['away_team_api_id', 'date', 'away_shoton', 'away_shotoff', 'away_cross', 'away_foulcommit', 'away_corner']]
    return stats.rename(columns=lambda col: col.replace('away_', ""))


def create_stats_columns(data, stat):
    away_stat = data.apply(partial(calculate_stat_away, stat), axis=1)
    home_stat = data.apply(partial(calculate_stat_home, stat), axis=1)
    return {'away_' + stat: away_stat, 'home_' + stat: home_stat}

def extract_n_previous_matches(stats, team_id, match_date, n=5):
    if team_id in stats: 
        team_stats = stats[team_id].truncate(before=match_date).sort_index(ascending=False)
        
        return team_stats.iloc[1:min(len(team_stats), n+1)].sum()

def extract_stats_by_match( stats, match):
    away = extract_n_previous_matches(stats, int(match['away_team_api_id']), datetime.strptime(match['date'],'%Y-%m-%d %H:%M:%S'))\
    .rename(lambda col: 'away_'+col)
    
    home = extract_n_previous_matches(stats, int(match['home_team_api_id']), datetime.strptime(match['date'],'%Y-%m-%d %H:%M:%S'))\
    .rename(lambda col: 'home_'+col)
    return home.append(away)

import  getsizeof from sys
getsizeof('A')


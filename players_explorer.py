 players_columns = ['home_player_1',
          'home_player_2','home_player_3','home_player_4',
          'home_player_5','home_player_6','home_player_7',
          'home_player_8','home_player_9','home_player_10',
          'home_player_11','away_player_1','away_player_2',
          'away_player_3','away_player_4','away_player_5',
          'away_player_6','away_player_7','away_player_8',
          'away_player_9','away_player_10','away_player_11']

def extract_players_features(complete_matches, reducer, players_stats):
    complete_matches[players_columns].apply(lambda player:players_stats.iloc[ ,axis=0)
    reducer.transform(players_stats.iloc[complete_matches.iloc[1]['home_player_1'].astype(int)])
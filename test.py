con = sqlite3.connect('./data/database.sqlite')

df = pd.read_sql_query("SELECT * FROM Match m", con)

labels = df.apply(calculate_label, axis=1)

stat_columns = join(map(lambda stat: create_stats_columns(df, stat), _STATS_COLUMNS_))

matches = df.assign(**stat_columns)
""" find all the teams"""
teams = pd.read_sql_query("SELECT team_api_id FROM Team", con)
stats_by_team_dict = dict([(team_id, extract_stats_by_team_id(matches, team_id)) for team_id in teams['team_api_id']])

print extract_n_previous_matches(stats_by_team_dict, 9906, datetime(2016, 5, 14))

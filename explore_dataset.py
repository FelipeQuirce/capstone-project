import sqlite3
from tabulate import tabulate
import pandas as pd
import re


con = sqlite3.connect('database.sqlite')



df = pd.read_sql_query("select * from Match m where abs(m.away_player_11) <> 0 limit 1;", con)

player_headers = [x for x in df.keys().tolist() if re.match('.*?_player_\dx)]

print(df[player_headers])
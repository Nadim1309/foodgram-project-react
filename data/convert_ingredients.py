import sqlite3

import pandas as pd

conn = sqlite3.connect('backend/db.sqlite3')
c = conn.cursor()

genre = pd.read_csv('data/ingredients.csv')
genre.to_sql('recipes_ingredient', conn, if_exists='append', index=False)

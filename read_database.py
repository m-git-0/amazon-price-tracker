import sqlite3
import pandas as pd

def read_db():
    #connect to the database
    conn = sqlite3.connect('amztracker.db')

    df = pd.read_sql_query('''SELECT * FROM prices''',conn)
    print(df)
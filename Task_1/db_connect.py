import sqlite3

conn = sqlite3.connect("pft.db")

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS finances
(id INTEGER PRIMARY KEY,
Date DATE, 
category TEXT,
income FLOAT,
expense FLOAT) 
""")

conn.commit()
conn.close()
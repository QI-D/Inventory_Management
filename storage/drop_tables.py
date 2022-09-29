import sqlite3

conn = sqlite3.connect('business.sqlite')

c = conn.cursor()
c.execute('''DROP TABLE revenue''')

conn.commit()
conn.close()

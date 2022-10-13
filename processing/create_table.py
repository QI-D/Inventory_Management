import sqlite3

conn = sqlite3.connect('stats.sqlite')

c = conn.cursor()
# c.execute('''
#           CREATE TABLE stats
#           (id INTEGER PRIMARY KEY ASC,
#            total_expense DECIMAL NOT NULL,
#            total_item INT NOT NULL,
#            popular_item VARCHAR(100) NOT NULL,
#            max_quantity INT NOT NULL,
#            daily_revenue VARCHAR(100) NOT NULL,
#            last_updated VARCHAR(100) NOT NULL)
#           ''')
c.execute('''
          CREATE TABLE stats
          (id INTEGER PRIMARY KEY ASC,
           total_expense DECIMAL NOT NULL,
           total_item VARCHAR(100) NOT NULL,
           popular_item VARCHAR(100) NOT NULL,
           max_quantity INT NOT NULL,
           daily_revenue DECIMAL NOT NULL,
           last_updated VARCHAR(100) NOT NULL)
          ''')
conn.commit()
conn.close()

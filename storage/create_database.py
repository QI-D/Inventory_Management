import sqlite3

conn = sqlite3.connect('business.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE expense
          (id INTEGER PRIMARY KEY ASC, 
           order_id VARCHAR(36) NOT NULL,
           item_id VARCHAR(36) NOT NULL,
           item_name VARCHAR(250) NOT NULL,
           quantity INTEGER NOT NULL,
           price DECIMAL NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE revenue
          (id INTEGER PRIMARY KEY ASC,
           submission_id VARCHAR(36) NOT NULL,
           store_id VARCHAR(20) NOT NULL,
           employee_id VARCHAR(20) NOT NULL,
           revenue DECIMAL NOT NULL,
           report_period INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()

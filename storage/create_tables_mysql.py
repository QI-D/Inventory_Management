import mysql.connector
import yaml

with open('app_config.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

db_conn = mysql.connector.connect(host=app_config["datastore"]["host"],
                                  user=app_config["datastore"]["user"],
                                  password=app_config["datastore"]["hostname"],
                                  database=app_config["datastore"]["db"])

db_cursor = db_conn.cursor()

db_cursor.execute('''
          CREATE TABLE expense
          (id INT NOT NULL AUTO_INCREMENT,
           order_id VARCHAR(36) NOT NULL,
           item_id VARCHAR(36) NOT NULL,
           item_name VARCHAR(250) NOT NULL,
           quantity INTEGER NOT NULL,
           price DECIMAL NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(36) NOT NULL,
           PRIMARY KEY (id))
          ''')

db_cursor.execute('''
          CREATE TABLE revenue
          (id INT NOT NULL AUTO_INCREMENT,
           submission_id VARCHAR(36) NOT NULL,
           store_id VARCHAR(20) NOT NULL,
           employee_id VARCHAR(20) NOT NULL,
           revenue DECIMAL NOT NULL,
           report_period INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(36) NOT NULL,
           PRIMARY KEY (id))
          ''')

db_conn.commit()
db_conn.close()

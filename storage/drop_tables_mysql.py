import mysql.connector
import yaml

with open('app_config.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

db_conn = mysql.connector.connect(host=app_config["datastore"]["host"],
                                  user=app_config["datastore"]["user"],
                                  password=app_config["datastore"]["hostname"],
                                  database=app_config["datastore"]["db"])

db_cursor = db_conn.cursor()
db_cursor.execute(''' DROP TABLE expense, revenue ''')
db_conn.commit()
db_conn.close()

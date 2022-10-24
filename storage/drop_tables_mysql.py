import mysql.connector

db_conn = mysql.connector.connect(host="ec2-34-230-81-97.compute-1.amazonaws.com",
                                  user="root",
                                  password="SecuRe_pwd1",
                                  database="inventory")

db_cursor = db_conn.cursor()
db_cursor.execute(''' DROP TABLE expense, revenue ''')
db_conn.commit()
db_conn.close()

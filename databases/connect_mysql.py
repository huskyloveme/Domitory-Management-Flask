import mysql.connector
from databases.info_db import db_config_info

db_config = db_config_info
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()
# query = "select count(1) from students"
# cursor.execute(query)
# result_col = cursor.fetchall()
# print(result_col)
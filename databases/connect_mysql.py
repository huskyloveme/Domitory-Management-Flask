import mysql.connector

db_config = {
    'host': '34.143.147.167',
    'user': 'admin',
    'password': 'Admin123!@#',
    'database': 'domitory_management',
    'port': '3306'
}
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()
# query = "select count(1) from students"
# cursor.execute(query)
# result_col = cursor.fetchall()
# print(result_col)
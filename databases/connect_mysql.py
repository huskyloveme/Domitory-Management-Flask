import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'data_craw'
}
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()
query = "select count(1) from final_data"
cursor.execute(query)
result_col = cursor.fetchall()
print(result_col)
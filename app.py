from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_parameter
from databases.connect_mysql import cursor, connection
import math


app = Flask(__name__, static_folder="static")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/show_database_<table_name>')
def show_database(table_name):
    page = request.args.get('page', 1, type=int)
    table_name = table_name
    limit = 15
    # Take the column name
    query = f"show columns FROM {table_name}"
    cursor.execute(query)
    result_col = cursor.fetchall()
    col = [i[0] for i in result_col]

    # Take the data
    query = f"select * from {table_name} limit " + str(limit) + " offset " + str(int(page-1)*limit)
    cursor.execute(query)
    result_data_col = cursor.fetchall()
    data_col = [i for i in result_data_col]

    #Count page_data
    query = f"select count(1) from {table_name}"
    cursor.execute(query)
    result_data_col = cursor.fetchall()
    count_data = int(result_data_col[0][0])

    return render_template("home/home.html", col=col, data_col=data_col, page = int(page), count_data=count_data, total_page=math.ceil(count_data/limit))




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
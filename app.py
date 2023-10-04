from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_parameter
from databases.connect_mysql import cursor, connection




app = Flask(__name__, template_folder='templates')


@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    limit = 15

    # Take the column name
    query = "show columns FROM final_data"
    cursor.execute(query)
    result_col = cursor.fetchall()
    col = [i[0] for i in result_col]

    # Take the data
    query = "select * from final_data limit " + str(limit) + " offset " + str(int(page)*limit)
    cursor.execute(query)
    result_data_col = cursor.fetchall()
    data_col = [i for i in result_data_col]

    #Count page_data
    query = "select count(1) from final_data"
    cursor.execute(query)
    result_data_col = cursor.fetchall()
    count_data = int(result_data_col[0][0])

    return render_template("home/home.html", col=col, data_col=data_col, page = int(page), count_data=count_data, total_page=round(count_data/limit))




if __name__ == '__main__':
    app.run(debug=True)
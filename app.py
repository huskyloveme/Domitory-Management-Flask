from flask import Flask, render_template, request, jsonify
# from flask_paginate import Pagination, get_page_parameter
from databases.connect_mysql import cursor, connection
import math
from datetime import datetime

app = Flask(__name__, static_folder="static")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/show_database_<table_name>')
def show_database(table_name):
    page = request.args.get('page', 1, type=int)
    limit = 15
    # # Take the column name
    # query = f"SHOW COLUMNS FROM {table_name}"
    # cursor.execute(query)
    # result_col = cursor.fetchall()
    # col = [i[0] for i in result_col]
    # col.append('Edit')
    # col.append('Delete')
    # Take the data
    query = f"SELECT * FROM {table_name} LIMIT " + str(limit) + " OFFSET " + str(int(page-1)*limit)
    if table_name == 'students':
        query = f"SELECT t.id, t.msv,t.name,t.address,t.phone,t.gender,t.birthday,t.day_in,t.day_out,t.status,tt.name as room, t.created_at,t.updated_at \
         FROM {table_name} as t LEFT JOIN rooms as tt on t.room_id = tt.id LIMIT " + str(limit) + " OFFSET " + str(int(page - 1) * limit)
    cursor.execute(query)

    col = [column[0] for column in cursor.description]
    col.append('Edit')
    col.append('Delete')

    result_data_col = cursor.fetchall()
    data_col = [i for i in result_data_col]

    #Count page_data
    query = f"SELECT COUNT(1) FROM {table_name}"
    cursor.execute(query)
    result_data_col = cursor.fetchall()
    count_data = int(result_data_col[0][0])

    return render_template("home/show_database.html",
                           table_name = table_name,
                           col=col,
                           data_col=data_col,
                           page = int(page),
                           count_data=count_data,
                           total_page=math.ceil(count_data / limit)
                           )


@app.route('/<table_name>_add', methods=['POST', 'GET'])
def add_data(table_name):
    if request.method == "GET":
        # Take the column name
        query = f"SHOW COLUMNS FROM {table_name}"
        cursor.execute(query)
        result_col = cursor.fetchall()
        col = [i[0] for i in result_col[1:-2]]

        return render_template("home/add_database.html",
                               table_name=table_name,
                               col = col,
                               )

    if request.method == "POST":
        response = {
            "ok": False,
            "mesg": "Nothing",
            "data": []
        }
        if table_name == 'students':
            try:
                room_id = request.form.get('room_id')
                msv = request.form.get('msv')
                name = request.form.get('name')
                address = request.form.get('address')
                phone = request.form.get('phone')
                gender = request.form.get('gender')
                birthday = datetime.strptime(request.form.get('birthday'), '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('birthday') != '' else None
                day_in = datetime.strptime(request.form.get('day_in'), '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('day_in') != '' else None
                day_out = datetime.strptime(request.form.get('day_out'), '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('day_out') != '' else None
                status = request.form.get('status')

                query_add = "INSERT INTO " + table_name + " (room_id, msv, name, address, phone, gender, status, birthday, day_in, day_out) VALUES (" \
                            + "'" + room_id +"'," \
                            + "'" + msv +"'," \
                            + "'" + name +"'," \
                            + "'" + address +"'," \
                            + "'" + phone +"'," \
                            + "'" + gender +"'," \
                            + "'" + status +"'," \
                            + (("'" + birthday +"',") if birthday else 'null,') \
                            + (("'" + day_in +"',") if day_in else 'null,') \
                            + (("'" + day_out + "')") if day_out else 'null)')
                cursor.execute(query_add)
                connection.commit()
                response = {
                    "ok": True,
                    "mesg": "Add successfully",
                    "data": []
                }

            except Exception as err:
                response = {
                    "ok": False,
                    "mesg": str(err),
                    "data": []
                }
        if table_name == 'rooms':
            try:
                building_id = request.form.get('building_id')
                name = request.form.get('name')
                accommodate = request.form.get('accommodate')
                type = request.form.get('type')
                capacity = request.form.get('capacity')
                price = request.form.get('price')
                status = request.form.get('status')

                query_add = "INSERT INTO " + table_name + " (building_id, name, accommodate, type, capacity, price, status) VALUES (" \
                            + (("'" + building_id +"',") if building_id else 'null,') \
                            + "'" + name +"'," \
                            + (("'" + accommodate +"',") if accommodate else 'null,') \
                            + "'" + type +"'," \
                            + "'" + capacity +"'," \
                            + "'" + price +"'," \
                            + "'" + status +"'" \
                            + ")"

                cursor.execute(query_add)
                connection.commit()
                response = {
                    "ok": True,
                    "mesg": "Add successfully",
                    "data": []
                }

            except Exception as err:
                response = {
                    "ok": False,
                    "mesg": str(err),
                    "data": []
                }
        if table_name == 'buildings':
            try:
                name = request.form.get('name')
                address = request.form.get('address')
                query_add = "INSERT INTO " + table_name + " (name, address) VALUES (" \
                            + "'" + name + "'," \
                            + "'" + address + "'" \
                            + ")"

                cursor.execute(query_add)
                connection.commit()
                response = {
                    "ok": True,
                    "mesg": "Add successfully",
                    "data": []
                }

            except Exception as err:
                response = {
                    "ok": False,
                    "mesg": str(err),
                    "data": []
                }
        if table_name == 'motorbikes':
            try:
                # msv =
                name = request.form.get('name')
                address = request.form.get('address')
                query_add = "INSERT INTO " + table_name + " (name, address) VALUES (" \
                            + "'" + name + "'," \
                            + "'" + address + "'" \
                            + ")"

                cursor.execute(query_add)
                connection.commit()
                response = {
                    "ok": True,
                    "mesg": "Add successfully",
                    "data": []
                }

            except Exception as err:
                response = {
                    "ok": False,
                    "mesg": str(err),
                    "data": []
                }

        return jsonify(response)

@app.route('/<table_name>_edit_<id>', methods=['POST', 'GET'])
def edit_data(table_name, id):
    if request.method == 'GET':
        # Take the data
        query = f"SELECT * FROM {table_name} WHERE id = {id}"
        if table_name == 'students':
            query = "SELECT t.id, t.msv,t.name,t.address,t.phone,t.gender,t.birthday,t.day_in,t.day_out,t.status,tt.name as room, t.created_at,t.updated_at \
                     FROM students as t  left join rooms as tt on t.room_id = tt.id WHERE t.id = " + str(id)
        cursor.execute(query)

        column_names = [column[0] for column in cursor.description[1:-2]]

        result_row = cursor.fetchone()

        result_dict = {column_names[i]: result_row[i+1] for i in range(len(column_names))}

        return render_template("home/edit_database.html",
                               table_name=table_name,
                               data = result_dict,
                               )
    if request.method == 'POST':
        response = {
            "ok": False,
            "mesg": "Nothing",
            "data": []
        }
        if table_name == 'students':
            try:
                room = request.form.get('room')
                msv = request.form.get('msv')
                name = request.form.get('name')
                address = request.form.get('address')
                phone = request.form.get('phone')
                gender = request.form.get('gender')

                try:
                    birthday = datetime.strptime(request.form.get('birthday'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('birthday') != '' else None
                except:
                    birthday = datetime.strptime(request.form.get('birthday'), '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('birthday') != '' else None

                try:
                    day_in = datetime.strptime(request.form.get('day_in'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('day_in') != '' else None
                except:
                    day_in = datetime.strptime(request.form.get('day_in'), '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('day_in') != '' else None

                try:
                    day_out = datetime.strptime(request.form.get('day_out'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('day_out') != '' else None
                except:
                    day_out = datetime.strptime(request.form.get('day_out'), '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('day_out') != '' else None
                status = request.form.get('status')
                update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # query_check = (SELECT COUNT(*) FROM rooms WHERE name = '" + room + "') > 0;"


                query_edit = "UPDATE " + table_name + " SET " \
                             + "room_id = (select id from rooms where name = '" + room + "')," \
                             + "msv = '" + msv + "'," \
                             + "name = '" + name + "'," \
                             + "address = '" + address + "'," \
                             + "phone = '" + phone + "'," \
                             + "gender = '" + gender + "'," \
                             + "status = '" + status + "'," \
                             + "updated_at = '" + update_at + "'," \
                             + "birthday = " + (("'" + birthday + "',") if birthday else 'null,') \
                             + "day_in = " + (("'" + day_in + "',") if day_in else 'null,') \
                             + "day_out = " + (("'" + day_out + "'") if day_out else 'null ') \
                             + "WHERE id = " + id + " " \
                             + "AND (SELECT COUNT(*) FROM rooms WHERE name = '" + room + "') > 0;"
                cursor.execute(query_edit)
                connection.commit()
                response = {
                    "ok": True,
                    "mesg": "Edit successfully",
                    "data": []
                }
            except Exception as err:
                response = {
                    "ok": False,
                    "mesg": str(err),
                    "data": []
                }

        if table_name == 'rooms':
            try:
                building_id = request.form.get('building_id')
                name = request.form.get('name')
                accommodate = request.form.get('accommodate')
                type = request.form.get('type')
                capacity = request.form.get('capacity')
                price = request.form.get('price')
                status = request.form.get('status')
                update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                query_edit = "UPDATE " + table_name + " SET " \
                             + "building_id = " + (("'" + building_id + "',") if building_id else 'null,') \
                             + "name = '" + name + "'," \
                             + "accommodate = " + (("'" + accommodate + "',") if accommodate else 'null,') \
                             + "type = '" + type + "'," \
                             + "capacity = '" + capacity + "'," \
                             + "price = '" + price + "'," \
                             + "updated_at = '" + update_at + "'," \
                             + "status = '" + status + "'" \
                             + "WHERE id = " + id

                cursor.execute(query_edit)
                connection.commit()
                response = {
                    "ok": True,
                    "mesg": "Edit successfully",
                    "data": []
                }

            except Exception as err:
                response = {
                    "ok": False,
                    "mesg": str(err),
                    "data": []
                }
        if table_name == 'buildings':
            try:
                name = request.form.get('name')
                address = request.form.get('address')
                query_edit = "UPDATE " + table_name + " SET " \
                             + "name = '" + name + "'," \
                             + "address = '" + address + "'" \
                             + "WHERE id = " + id

                cursor.execute(query_edit)
                connection.commit()
                response = {
                    "ok": True,
                    "mesg": "Edit successfully",
                    "data": []
                }

            except Exception as err:
                response = {
                    "ok": False,
                    "mesg": str(err),
                    "data": []
                }
        return jsonify(response)


@app.route('/<table_name>_delete_<id>', methods=['POST'])
def delete_data(table_name, id):
    if request.method == "POST":
        if table_name == 'students' or table_name == 'rooms' or table_name == 'buildings':
            try:
                response = {
                    "ok": False,
                    "mesg": "Nothing",
                    "data": []
                }
                query_delete = "DELETE FROM " + table_name + " WHERE id = " + id
                cursor.execute(query_delete)
                connection.commit()
                response = {
                    "ok": True,
                    "mesg": "Delete successfully",
                    "data": []
                }
            except Exception as err:
                response = {
                    "ok": False,
                    "mesg": str(err),
                    "data": []
                }
            return jsonify(response)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
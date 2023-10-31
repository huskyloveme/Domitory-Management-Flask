from flask import Flask, render_template, request, jsonify
# from flask_paginate import Pagination, get_page_parameter
# from databases.connect_mysql import cursor, connection
import math
from datetime import datetime

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'host': os.getenv('host'),
    'database': os.getenv('database'),
    'port': os.getenv('port')
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()



app = Flask(__name__, static_folder="static")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/free_query', methods = ['GET','POST'])
def free_query():
    if request.method == "GET":
        return render_template("home/advance_request.html")

    if request.method == "POST":
        try:
            response = {
                "ok": False,
                "mesg": "Nothing",
                "data": []
            }
            query = request.form.get('query')
            cursor.execute(query)
            col = [column[0] for column in cursor.description]
            result_data_col = cursor.fetchall()
            data_col = [i for i in result_data_col]
            data = render_template("home/show_db.html",
                                   col=col,
                                   data_col=data_col)
            response = {
                "ok": True,
                "mesg": "Successfully",
                "data": data
            }
        except Exception as err:
            response = {
                "ok": False,
                "mesg": str(err),
                "data": []
            }
        return jsonify(response)

@app.route('/show_database_<table_name>')
def show_database(table_name):
    page = request.args.get('page', 1, type=int)
    limit = 15
    # Take the data
    query = f"SELECT * FROM {table_name} LIMIT " + str(limit) + " OFFSET " + str(int(page-1)*limit)
    if table_name == 'students':
        query = f"SELECT t.id, t.msv,t.name,t.address,t.phone,t.gender,t.birthday,t.day_in,t.day_out,t.status,tt.name as room, t.created_at,t.updated_at \
         FROM {table_name} as t LEFT JOIN rooms as tt on t.room_id = tt.id LIMIT " + str(limit) + " OFFSET " + str(int(page - 1) * limit)
    if table_name == 'rooms':
        query = f"SELECT t.id,t.name,t.accommodate,t.type,t.capacity,t.price,t.status,tt.name as building, t.created_at,t.updated_at \
         FROM {table_name} as t LEFT JOIN buildings as tt on t.building_id = tt.id LIMIT " + str(limit) + " OFFSET " + str(int(page - 1) * limit)
    if table_name == 'buildings':
        query = f"SELECT id,name,address,created_at,updated_at FROM {table_name} LIMIT " + str(limit) + " OFFSET " + str(int(page - 1) * limit)
    if table_name == 'motorbikes':
        query = f"SELECT t.id,t.license_plate,t.name,t.time_registration,t.status, tt.msv as msv, t.created_at,t.updated_at \
         FROM {table_name} as t LEFT JOIN students as tt on t.student_id = tt.id LIMIT " + str(limit) + " OFFSET " + str(int(page - 1) * limit)
    if table_name == 'visitors':
        query = f"SELECT t.id,t.cccd,t.name	,t.phone,t.gender,t.time_in,t.time_out, tt.msv as friend_of_msv, t.created_at,t.updated_at \
         FROM {table_name} as t LEFT JOIN students as tt on t.student_id = tt.id LIMIT " + str(limit) + " OFFSET " + str(int(page - 1) * limit)
    if table_name == 'parking_histories':
        query = f"SELECT t.id,tt.license_plate as license_plate,t.time_in,t.time_out, t.status,t.price, t.created_at,t.updated_at \
         FROM {table_name} as t LEFT JOIN motorbikes as tt on t.motorbike_id = tt.id LIMIT " + str(limit) + " OFFSET " + str(int(page - 1) * limit)
    if table_name == 'services':
        query = f"SELECT id,name,price,unit,description,created_at,updated_at FROM {table_name} LIMIT " + str(limit) + " OFFSET " + str(int(page - 1) * limit)
    if table_name == 'student_service':
        query = f"SELECT t.id,tt.msv as msv,ttt.name as service, t.time_use,t.time_end,t.created_at,t.updated_at \
         FROM {table_name} as t LEFT JOIN students as tt on t.student_id = tt.id LEFT JOIN services as ttt on t.service_id = ttt.id LIMIT " + str(limit) + " OFFSET " + str(int(page - 1) * limit)
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
        if table_name == 'students':
            query = "SELECT t.msv,t.name,t.address,t.phone,t.gender,t.birthday,t.day_in,t.day_out,t.status,tt.name as room \
                     FROM students as t  left join rooms as tt on t.room_id = tt.id"
            cursor.execute(query)
            col = [column[0] for column in cursor.description]
            results = cursor.fetchall()
            # ======================
            query_data_room = "SELECT name FROM rooms ORDER BY name"
            cursor.execute(query_data_room)
            result_col_data_room = cursor.fetchall()
            data_room = [column[0] for column in result_col_data_room]
            data_room.append('None')
            return render_template("home/add_database.html",
                                   table_name=table_name,
                                   col=col,
                                   data_room=data_room
                                   )
        elif table_name == 'rooms':
            query = "SELECT t.name,t.accommodate,t.type,t.capacity,t.price,t.status,tt.name as building FROM rooms as t  left join buildings as tt on t.building_id = tt.id"
            cursor.execute(query)
            col = [column[0] for column in cursor.description]
            results = cursor.fetchall()
            # ======================
            query_data_room = "SELECT name FROM buildings ORDER BY name"
            cursor.execute(query_data_room)
            result_col_data_building = cursor.fetchall()
            data_building = [column[0] for column in result_col_data_building]
            data_building.append('None')
            return render_template("home/add_database.html",
                                   table_name=table_name,
                                   col=col,
                                   data_building=data_building
                                   )
        elif table_name == 'buildings':
            query = "SELECT name,address FROM buildings"
            cursor.execute(query)
            col = [column[0] for column in cursor.description]
            results = cursor.fetchall()
            return render_template("home/add_database.html",
                                   table_name=table_name,
                                   col=col,
                                   )
        elif table_name == 'motorbikes':
            query = "SELECT t.license_plate,t.name,t.time_registration,t.status,tt.msv as msv FROM motorbikes as t  left join students as tt on t.student_id = tt.id"
            cursor.execute(query)
            col = [column[0] for column in cursor.description]
            results = cursor.fetchall()
            # ======================
            query_data_sinhvien = "SELECT msv FROM students ORDER BY msv"
            cursor.execute(query_data_sinhvien)
            result_col_data_sinhvien = cursor.fetchall()
            data_sinhvien = [column[0] for column in result_col_data_sinhvien]
            return render_template("home/add_database.html",
                                   table_name=table_name,
                                   col=col,
                                   data_sinhvien=data_sinhvien
                                   )
        elif table_name == 'visitors':
            query = "SELECT t.cccd,t.name,t.phone,t.gender,t.time_in,t.time_out,tt.msv as friend_of_msv FROM visitors as t  left join students as tt on t.student_id = tt.id"
            cursor.execute(query)
            col = [column[0] for column in cursor.description]
            results = cursor.fetchall()
            # ======================
            query_data_sinhvien = "SELECT msv FROM students ORDER BY msv"
            cursor.execute(query_data_sinhvien)
            result_col_data_sinhvien = cursor.fetchall()
            data_sinhvien = [column[0] for column in result_col_data_sinhvien]
            return render_template("home/add_database.html",
                                   table_name=table_name,
                                   col=col,
                                   data_sinhvien=data_sinhvien
                                   )
        elif table_name == 'parking_histories':
            query = "SELECT tt.license_plate as license_plate,t.time_in,t.time_out FROM parking_histories as t  left join motorbikes as tt on t.motorbike_id = tt.id"
            cursor.execute(query)
            col = [column[0] for column in cursor.description]
            results = cursor.fetchall()
            # ======================
            query_data_motor = "SELECT license_plate FROM motorbikes ORDER BY license_plate"
            cursor.execute(query_data_motor)
            result_col_data_motor = cursor.fetchall()
            data_motor = [column[0] for column in result_col_data_motor]
            return render_template("home/add_database.html",
                                   table_name=table_name,
                                   col=col,
                                   data_motor=data_motor
                                   )
        elif table_name == 'services':
            query = "SELECT name,price,unit,description FROM services"
            cursor.execute(query)
            col = [column[0] for column in cursor.description]
            results = cursor.fetchall()
            return render_template("home/add_database.html",
                                   table_name=table_name,
                                   col=col,
                                   )
        elif table_name == 'student_service':
            query = "SELECT tt.msv as msv, ttt.name as service, t.time_use,t.time_end FROM student_service as t  left join students as tt on t.student_id = tt.id left join services as ttt on t.service_id = ttt.id"
            cursor.execute(query)
            col = [column[0] for column in cursor.description]
            results = cursor.fetchall()
            # ======================
            query_data_service = "SELECT name FROM services ORDER BY name"
            cursor.execute(query_data_service)
            result_col_data_service = cursor.fetchall()
            data_service = [column[0] for column in result_col_data_service]
            # ======================
            query_data_sinhvien = "SELECT msv FROM students ORDER BY msv"
            cursor.execute(query_data_sinhvien)
            result_col_data_sinhvien = cursor.fetchall()
            data_sinhvien = [column[0] for column in result_col_data_sinhvien]
            return render_template("home/add_database.html",
                                   table_name=table_name,
                                   col=col,
                                   data_service=data_service,
                                   data_sinhvien=data_sinhvien,
                                   )
        else:
            return "404 NOT FOUND!!!"

    if request.method == "POST":
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

                query_add = "INSERT INTO " + table_name + " (room_id, msv, name, address, phone, gender, status, birthday, day_in, day_out) VALUES (" \
                            + "(SELECT id FROM rooms where name = '" + room +"')," \
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
                building = request.form.get('building')
                name = request.form.get('name')
                accommodate = request.form.get('accommodate')
                type = request.form.get('type')
                capacity = request.form.get('capacity')
                price = request.form.get('price')
                status = request.form.get('status')

                query_add = "INSERT INTO " + table_name + " (building_id, name, accommodate, type, capacity, price, status) VALUES (" \
                            + "(SELECT id FROM buildings WHERE name = '" + building +"')," \
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
                msv = request.form.get('msv')
                license_plate = request.form.get('license_plate')
                name = request.form.get('name')
                try:
                    time_registration = datetime.strptime(request.form.get('time_registration'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('time_registration') != '' else None
                except:
                    time_registration = datetime.strptime(request.form.get('time_registration'), '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('time_registration') != '' else None
                status = request.form.get('status')
                query_add = "INSERT INTO " + table_name + " (student_id,license_plate, name, time_registration, status) VALUES (" \
                            + "(SELECT id FROM students WHERE msv = '" + msv +"')," \
                            + "'" + license_plate + "'," \
                            + "'" + name + "'," \
                            + "'" + time_registration + "'," \
                            + "'" + status + "'" \
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
        if table_name == 'visitors':
            try:
                cccd = request.form.get('cccd')
                name = request.form.get('name')
                phone = request.form.get('phone')
                gender = request.form.get('gender')
                try:
                    time_in = datetime.strptime(request.form.get('time_in'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('time_in') != '' else None
                except:
                    time_in = datetime.strptime(request.form.get('time_in'), '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('time_in') != '' else None
                try:
                    time_out = datetime.strptime(request.form.get('time_out'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('time_out') != '' else None
                except:
                    time_out = datetime.strptime(request.form.get('time_out'), '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('time_out') != '' else None
                friend_of_msv = request.form.get('friend_of_msv')

                query_add = "INSERT INTO " + table_name + " (student_id,cccd,name, phone, gender, time_in,time_out) VALUES (" \
                            + "(SELECT id FROM students WHERE msv = '" + friend_of_msv +"')," \
                            + "'" + cccd + "'," \
                            + "'" + name + "'," \
                            + "'" + phone + "'," \
                            + "'" + gender + "'," \
                            + (("'" + time_in +"',") if time_in else 'null,') \
                            + (("'" + time_out +"'") if time_out else 'null') \
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
        if table_name == 'parking_histories':
            try:
                license_plate = request.form.get('license_plate')
                try:
                    time_in = datetime.strptime(request.form.get('time_in'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('time_in') != '' else None
                except:
                    time_in = datetime.strptime(request.form.get('time_in'), '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('time_in') != '' else None
                try:
                    time_out = datetime.strptime(request.form.get('time_out'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('time_out') != '' else None
                except:
                    time_out = datetime.strptime(request.form.get('time_out'), '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('time_out') != '' else None

                query_add = "INSERT INTO " + table_name + " (motorbike_id,time_in,time_out, status, price) VALUES (" \
                            + "(SELECT id FROM motorbikes WHERE license_plate = '" + license_plate +"')," \
                            + (("'" + time_in +"',") if time_in else 'null,') \
                            + (("'" + time_out +"',") if time_out else 'null,') \
                            + "'FREE'," \
                            + "'0'" \
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
        if table_name == 'services':
            try:
                name = request.form.get('name')
                price = request.form.get('price')
                unit = request.form.get('unit')
                description = request.form.get('description')
                query_add = "INSERT INTO " + table_name + " (name,price,unit,description) VALUES (" \
                            + "'" + name + "'," \
                            + "'" + price + "'," \
                            + "'" + unit + "'," \
                            + "'" + description + "'" \
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
        if table_name == 'student_service':
            try:
                msv = request.form.get('msv')
                service = request.form.get('service')
                time_use = request.form.get('time_use')
                try:
                    time_end = datetime.strptime(request.form.get('time_end'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('time_end') != '' else None
                except:
                    time_end = datetime.strptime(request.form.get('time_end'), '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('time_end') != '' else None

                query_add = "INSERT INTO " + table_name + " (student_id,service_id,time_use, time_end) VALUES (" \
                            + "(SELECT id FROM students WHERE msv = '" + msv +"')," \
                            + "(SELECT id FROM services WHERE name = '" + service + "')," \
                            + "'" + time_use + "'," \
                            + (("'" + time_end +"'") if time_end else 'null') \
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
        if table_name == 'students':
            query = "SELECT t.msv,t.name,t.address,t.phone,t.gender,t.birthday,t.day_in,t.day_out,t.status,tt.name as room \
                     FROM students as t  left join rooms as tt on t.room_id = tt.id WHERE t.id = " + str(id)
            cursor.execute(query)
            column_names = [column[0] for column in cursor.description]
            result_row = cursor.fetchone()
            result_dict = {column_names[i]: result_row[i] for i in range(len(column_names))}
            # ======================
            query_data_room = "SELECT name FROM rooms ORDER BY name"
            cursor.execute(query_data_room)
            result_col_data_room = cursor.fetchall()
            data_room = [column[0] for column in result_col_data_room]
            data_room.append('None')
            return render_template("home/edit_database.html",
                                   table_name=table_name,
                                   data=result_dict,
                                   data_room=data_room,
                                   )
        if table_name == 'rooms':
            query = "SELECT t.name,t.accommodate,t.type,t.capacity,t.price,t.status,tt.name as building FROM rooms as t  left join buildings as tt on t.building_id = tt.id WHERE t.id = " + str(id)
            cursor.execute(query)
            column_names = [column[0] for column in cursor.description]
            result_row = cursor.fetchone()
            result_dict = {column_names[i]: result_row[i] for i in range(len(column_names))}
            # ======================
            query_data_room = "SELECT name FROM buildings ORDER BY name"
            cursor.execute(query_data_room)
            result_col_data_building = cursor.fetchall()
            data_building = [column[0] for column in result_col_data_building]
            data_building.append('None')
            return render_template("home/edit_database.html",
                                   table_name=table_name,
                                   data=result_dict,
                                   data_building=data_building,
                                   )
        if table_name == 'buildings':
            query = "SELECT name,address FROM buildings WHERE id = " + str(id)
            cursor.execute(query)
            column_names = [column[0] for column in cursor.description]
            result_row = cursor.fetchone()
            result_dict = {column_names[i]: result_row[i] for i in range(len(column_names))}
            return render_template("home/edit_database.html",
                                   table_name=table_name,
                                   data=result_dict,
                                   )
        if table_name == 'motorbikes':
            query = "SELECT t.license_plate,t.name,t.time_registration,t.status,tt.msv as msv FROM motorbikes as t  left join students as tt on t.student_id = tt.id WHERE t.id = " + str(id)
            cursor.execute(query)
            column_names = [column[0] for column in cursor.description]
            result_row = cursor.fetchone()
            result_dict = {column_names[i]: result_row[i] for i in range(len(column_names))}
            # ======================
            query_data_room = "SELECT msv FROM students ORDER BY msv"
            cursor.execute(query_data_room)
            result_col_data_building = cursor.fetchall()
            data_building = [column[0] for column in result_col_data_building]
            return render_template("home/edit_database.html",
                                   table_name=table_name,
                                   data=result_dict,
                                   data_sinhvien=data_building,
                                   )
        if table_name == 'visitors':
            query = "SELECT t.cccd,t.name,t.phone,t.gender,t.time_in,t.time_out,tt.msv as friend_of_msv FROM visitors as t  left join students as tt on t.student_id = tt.id WHERE t.id = " + str(id)
            cursor.execute(query)
            column_names = [column[0] for column in cursor.description]
            result_row = cursor.fetchone()
            result_dict = {column_names[i]: result_row[i] for i in range(len(column_names))}
            # ======================
            query_data_room = "SELECT msv FROM students ORDER BY msv"
            cursor.execute(query_data_room)
            result_col_data_building = cursor.fetchall()
            data_building = [column[0] for column in result_col_data_building]
            return render_template("home/edit_database.html",
                                   table_name=table_name,
                                   data=result_dict,
                                   data_sinhvien=data_building,
                                   )
        if table_name == 'parking_histories':
            query = "SELECT tt.license_plate as license_plate,t.time_in,t.time_out,t.status,t.price FROM parking_histories as t  left join motorbikes as tt on t.motorbike_id = tt.id WHERE t.id = " + str(id)
            cursor.execute(query)
            column_names = [column[0] for column in cursor.description]
            result_row = cursor.fetchone()
            result_dict = {column_names[i]: result_row[i] for i in range(len(column_names))}
            # ======================
            query_data_motor = "SELECT license_plate FROM motorbikes ORDER BY license_plate"
            cursor.execute(query_data_motor)
            result_col_data_motor = cursor.fetchall()
            data_motor = [column[0] for column in result_col_data_motor]
            return render_template("home/edit_database.html",
                                   table_name=table_name,
                                   data=result_dict,
                                   data_motor=data_motor
                                   )
        if table_name == 'services':
            query = "SELECT name,price,unit,description FROM services WHERE id = " + str(id)
            cursor.execute(query)
            column_names = [column[0] for column in cursor.description]
            result_row = cursor.fetchone()
            result_dict = {column_names[i]: result_row[i] for i in range(len(column_names))}
            return render_template("home/edit_database.html",
                                   table_name=table_name,
                                   data=result_dict,
                                   )
        if table_name == 'student_service':
            query = "SELECT tt.msv as msv, ttt.name as service, t.time_use,t.time_end FROM student_service as t  left join students as tt on t.student_id = tt.id left join services as ttt on t.service_id = ttt.id WHERE t.id = " + str(id)
            cursor.execute(query)
            column_names = [column[0] for column in cursor.description]
            result_row = cursor.fetchone()
            result_dict = {column_names[i]: result_row[i] for i in range(len(column_names))}
            # ======================
            query_data_service = "SELECT name FROM services ORDER BY name"
            cursor.execute(query_data_service)
            result_col_data_service = cursor.fetchall()
            data_service = [column[0] for column in result_col_data_service]
            # ======================
            query_data_sinhvien = "SELECT msv FROM students ORDER BY msv"
            cursor.execute(query_data_sinhvien)
            result_col_data_sinhvien = cursor.fetchall()
            data_sinhvien = [column[0] for column in result_col_data_sinhvien]
            return render_template("home/edit_database.html",
                                   table_name=table_name,
                                   data=result_dict,
                                   data_service=data_service,
                                   data_sinhvien=data_sinhvien,
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
        if table_name == 'rooms':
            try:
                building = request.form.get('building')
                name = request.form.get('name')
                accommodate = request.form.get('accommodate')
                type = request.form.get('type')
                capacity = request.form.get('capacity')
                price = request.form.get('price')
                status = request.form.get('status')
                update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                query_edit = "UPDATE " + table_name + " SET " \
                             + "building_id = (select id from buildings where name = '" + building + "')," \
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
        if table_name == 'motorbikes':
            try:
                msv = request.form.get('msv')
                license_plate = request.form.get('license_plate')
                name = request.form.get('name')
                try:
                    time_registration = datetime.strptime(request.form.get('time_registration'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('time_registration') != '' else None
                except:
                    time_registration = datetime.strptime(request.form.get('time_registration'), '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S') if request.form.get('time_registration') != '' else None
                status = request.form.get('status')
                updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                query_edit = "UPDATE " + table_name + " SET " \
                             + "student_id = (select id from students where msv = '" + msv + "')," \
                             + "license_plate = '" + license_plate + "'," \
                             + "name = '" + name + "'," \
                             + "time_registration = '" + time_registration + "'," \
                             + "updated_at = '" + updated_at + "'," \
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
        if table_name == 'visitors':
            try:
                cccd = request.form.get('cccd')
                name = request.form.get('name')
                phone = request.form.get('phone')
                gender = request.form.get('gender')
                try:
                    time_in = datetime.strptime(request.form.get('time_in'), '%Y-%m-%dT%H:%M:%S').strftime(
                        '%Y-%m-%d %H:%M:%S') if request.form.get('time_in') != '' else None
                except:
                    time_in = datetime.strptime(request.form.get('time_in'), '%Y-%m-%dT%H:%M').strftime(
                        '%Y-%m-%d %H:%M:%S') if request.form.get('time_in') != '' else None
                try:
                    time_out = datetime.strptime(request.form.get('time_out'), '%Y-%m-%dT%H:%M:%S').strftime(
                        '%Y-%m-%d %H:%M:%S') if request.form.get('time_out') != '' else None
                except:
                    time_out = datetime.strptime(request.form.get('time_out'), '%Y-%m-%dT%H:%M').strftime(
                        '%Y-%m-%d %H:%M:%S') if request.form.get('time_out') != '' else None
                friend_of_msv = request.form.get('friend_of_msv')
                updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                query_edit = "UPDATE " + table_name + " SET " \
                             + "student_id = (select id from students where msv = '" + friend_of_msv + "')," \
                             + "cccd = '" + cccd + "'," \
                             + "name = '" + name + "'," \
                             + "phone = '" + phone + "'," \
                             + "gender = '" + gender + "'," \
                             + "time_in = " + (("'" + time_in + "',") if time_in else 'null,') \
                             + "time_out = " + (("'" + time_out + "',") if time_out else 'null,') \
                             + "updated_at = '" + updated_at + "' " \
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
        if table_name == 'parking_histories':
            try:
                license_plate = request.form.get('license_plate')
                price = request.form.get('price')
                status = request.form.get('status')
                try:
                    time_in = datetime.strptime(request.form.get('time_in'), '%Y-%m-%dT%H:%M:%S').strftime(
                        '%Y-%m-%d %H:%M:%S') if request.form.get('time_in') != '' else None
                except:
                    time_in = datetime.strptime(request.form.get('time_in'), '%Y-%m-%dT%H:%M').strftime(
                        '%Y-%m-%d %H:%M:%S') if request.form.get('time_in') != '' else None
                try:
                    time_out = datetime.strptime(request.form.get('time_out'), '%Y-%m-%dT%H:%M:%S').strftime(
                        '%Y-%m-%d %H:%M:%S') if request.form.get('time_out') != '' else None
                except:
                    time_out = datetime.strptime(request.form.get('time_out'), '%Y-%m-%dT%H:%M').strftime(
                        '%Y-%m-%d %H:%M:%S') if request.form.get('time_out') != '' else None
                updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                query_edit = "UPDATE " + table_name + " SET " \
                             + "motorbike_id = (select id from motorbikes where license_plate = '" + license_plate + "')," \
                             + "price = '" + price + "'," \
                             + "status = '" + status + "'," \
                             + "time_in = " + (("'" + time_in + "',") if time_in else 'null,') \
                             + "time_out = " + (("'" + time_out + "',") if time_out else 'null,') \
                             + "updated_at = '" + updated_at + "' " \
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
        if table_name == 'services':
            try:
                name = request.form.get('name')
                price = request.form.get('price')
                unit = request.form.get('unit')
                description = request.form.get('description')
                query_edit = "UPDATE " + table_name + " SET " \
                             + "name = '" + name + "'," \
                             + "price = '" + price + "'," \
                             + "unit = '" + unit + "'," \
                             + "description = '" + description + "'" \
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
        if table_name == 'student_service':
            try:
                msv = request.form.get('msv')
                service = request.form.get('service')
                time_use = request.form.get('time_use')
                try:
                    time_end = datetime.strptime(request.form.get('time_end'), '%Y-%m-%dT%H:%M:%S').strftime(
                        '%Y-%m-%d %H:%M:%S') if request.form.get('time_end') != '' else None
                except:
                    time_end = datetime.strptime(request.form.get('time_end'), '%Y-%m-%dT%H:%M').strftime(
                        '%Y-%m-%d %H:%M:%S') if request.form.get('time_end') != '' else None
                updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                query_edit = "UPDATE " + table_name + " SET " \
                             + "student_id = (select id from students where msv = '" + msv + "')," \
                             + "service_id = (select id from services where name = '" + service + "')," \
                             + "time_use = '" + time_use + "'," \
                             + "time_end = " + (("'" + time_end + "',") if time_end else 'null,') \
                             + "updated_at = '" + updated_at + "' " \
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
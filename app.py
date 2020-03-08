import cx_Oracle
from flask import Flask, escape, request, render_template, send_from_directory

app = Flask(__name__, static_folder='static')

table_name = 'studenti'

connection = cx_Oracle.connect("student", "STUDENT", "localhost/XE")
cursor = connection.cursor()

get_columns = "select column_name from USER_TAB_COLUMNS where table_name = \'" + table_name.upper() + "\'"
cursor.execute(get_columns)
table_columns = [t[0] for t in [*cursor]]


def query_db(selected_columns: [], sort_by: []):
    get_tuples = "select " + ','.join(selected_columns) + " from " + table_name.upper()
    cursor.execute(get_tuples)
    tuples = [*cursor]
    return tuples


@app.route('/')
def home():
    tuples = query_db(table_columns, [])
    return render_template('index.html', tuples=tuples, columns=table_columns)


@app.route('/query_request', methods=['POST'])
def query_request():
    query_columns = request.json["columns"]
    if query_columns is None:
        return ''
    tuples = query_db(query_columns, [])
    return render_template('table.html', tuples=tuples, columns=query_columns)


@app.route('/<script_name>.js')
def get_script(script_name):
    return send_from_directory(app.static_folder, script_name + '.js')

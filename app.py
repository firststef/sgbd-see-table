import cx_Oracle
from flask import Flask, escape, request, render_template, send_from_directory

app = Flask(__name__, static_folder='static')

table_name = 'studenti'

connection = cx_Oracle.connect("student", "STUDENT", "localhost/XE")
cursor = connection.cursor()

get_columns = "select column_name from USER_TAB_COLUMNS where table_name = \'" + table_name.upper() + "\'"
cursor.execute(get_columns)
table_columns = [t[0] for t in [*cursor]]


def query_db(selected_columns: list, sort_by: dict, filter_values: dict):
    get_tuples = "select " + ','.join(selected_columns) + " from " + table_name.upper()
    filter_by_str = ''
    sort_by_str = ''

    new_dict = {}
    for f in filter_values:
        if filter_values[f] != '':
            new_dict['v_' + str(f).lower()] = filter_values[f]

    for column in selected_columns:
        if column in filter_values and filter_values[column] != '':
            filter_by_str += column + '=:v_' + str(column).lower() + ' and '
    if filter_by_str != '':
        filter_by_str = 'where ' + filter_by_str[:-5]

    for column in selected_columns:
        if column in sort_by and sort_by[column] != '':
            if sort_by[column] == 'asc' or sort_by[column] == 'desc':
                sort_by_str += column + ' ' + sort_by[column] + ','
    if sort_by_str != '':
        sort_by_str = 'order by ' + sort_by_str[:-1]

    query = get_tuples + ' ' + filter_by_str + ' ' + sort_by_str
    print(query)

    cursor.execute(query, **new_dict)
    tuples = [*cursor]

    return tuples, query


@app.route('/')
def home():
    tuples, query = query_db(table_columns, {}, {})

    print(cursor.callfunc('recommandation', str, [321]))

    return render_template('index.html', tuples=tuples, columns=table_columns, query=query)


@app.route('/query_request', methods=['POST'])
def query_request():
    print(request.json)
    query_columns = request.json["columns"]
    if query_columns is None:
        return ''

    try:
        tuples, query = query_db(query_columns, request.json["sort"], request.json["filters"])
    except BaseException:
        return 'query error'
    return render_template('table.html', tuples=tuples, columns=query_columns, query=query)


@app.route('/<script_name>.js')
def get_script(script_name):
    return send_from_directory(app.static_folder, script_name + '.js')

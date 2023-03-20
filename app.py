from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Reuben@1234'
app.config['MYSQL_DB'] = 'sports_management'

mysql = MySQL(app)
with open('tables.json', 'r') as f:
  tables_dict = json.load(f)

@app.route('/')
def index():
  return render_template('index.html')

@app.route("/display")
def display():
  table_data = {}
  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  for table_name in tables_dict:
    sql_query = "select * from {}".format(table_name)
    resultValue = cursor.execute(sql_query)
    current_table_data = []
    if resultValue > 0:
      current_table_data = cursor.fetchall()
      table_data[table_name] = list(current_table_data)
  return render_template('display.html', tables_dict = tables_dict, keys=tables_dict.keys(), table_data = table_data) #, task_data = task_data, task_keys = task_keys)

@app.route('/delete/<string:table_name>', methods=['GET', 'POST'])
def delete(table_name):
  if request.method == 'GET':
    args = request.args
    field_lst = []
    for attr in tables_dict[table_name]:
        field_value = args[attr]
        if (field_value == 'None' or field_value == None):
          field_value = None
        field_lst.append([attr, field_value])
    try:
      cur = mysql.connection.cursor()
      sql_query = 'delete from {} where '.format(table_name)
      for i in range(len(field_lst) - 1):
        if (field_lst[i][1]):
          sql_query = sql_query + field_lst[i][0] + '=' + '"' + field_lst[i][1] + '"' + ' and '
      if (field_lst[-1][1]):
        sql_query = sql_query + field_lst[-1][0] + '=' + '"' + field_lst[-1][1] + '";'
      elif (len(sql_query) > 4):
        sql_query = sql_query[:-5]
      cur.execute(sql_query)
      mysql.connection.commit()
      cur.close()
      return redirect('/display#' + str(table_name))
    except Exception as e:
      return 'There was an issue adding the entry:' + str(e)
  return redirect('/display#' + str(table_name))

@app.route('/update', methods=['GET', 'POST'])
def update():
  row = request.form['pk']
  name = ""
  id = ""
  col = ""
  idx = 0

  for i in row:
    if idx==0:
      if i != ",":
        name += i
      else:
        idx = 1
        continue
    if idx==1:
      if i != ",":
        id += i
      else:
        idx = 2
        continue
    if idx==2:
      if i != ",":
        col += i       
            
  value = request.form['value']
  cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  sql_query = 'update {2} set {3} = "{1}" where {4} = {0};'.format(id, value, name, col, tables_dict[name][0])

  try:
    cur.execute(sql_query)
    mysql.connection.commit()
    cur.close()
    return redirect('/#' + str(name))
  except:
    return redirect(request.url)

@app.route('/rename/<string:key>', methods=['GET', 'POST'])
def rename(key):
  print(key)
  msg = ''
  if request.method == 'POST':
    new_name = request.form['name']
    print(new_name)
    print("HI")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("ALTER TABLE {} RENAME {}".format(key, new_name))
    mysql.connection.commit()
    msg = 'You have successfully renamed the table !!'
    tables_dict[new_name] = tables_dict[key]
    del tables_dict[key]
    print(tables_dict)
    with open('tables.json', 'w') as json_file:
      json.dump(tables_dict, json_file)
    return redirect('/display#' + str(new_name))
  return render_template('rename.html', msg = msg, key = key)
  
if __name__ == "__main__":
  app.run(debug=True)
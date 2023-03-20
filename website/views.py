from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from . import db, tables_dict, mysql
import MySQLdb.cursors
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
def index():
    return render_template("index.html", user=current_user)

@views.route('/base-admin', methods=['GET','POST'])
@login_required
def admin_work():
    return render_template("admin_work.html",user=current_user, tables_dict = tables_dict )

@views.route("/display", methods=['GET','POST'])
@login_required
def display():
  msg =''
  table_data = {}
  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  for table_name in tables_dict:
    sql_query = "select * from {}".format(table_name)
    resultValue = cursor.execute(sql_query)
    
    current_table_data = []
    if resultValue > 0:
      current_table_data = cursor.fetchall()
      table_data[table_name] = list(current_table_data)
    mysql.connection.commit()
      
  if request.method == 'POST':
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    table_name = request.form.get('keyaa')
    
    column_name =tables_dict[table_name]
    data = []

    sql_query_insert = "INSERT INTO "+table_name+" VALUES ("+"% s,"*(len(column_name)-1)+"% s)"
    for i in column_name:
      data.append(request.form[i])
    data = tuple(data)
    try:
      cursor.execute(sql_query_insert,data)
      mysql.connection.commit()
      msg='Data inserted'
      print(msg)      
    except:
      msg = 'Data already exists'
      print(msg)

  return render_template('display.html', tables_dict = tables_dict, keys=tables_dict.keys(), table_data = table_data, user = current_user, msg =msg)

@views.route('/delete/<string:table_name>', methods=['GET', 'POST'])
@login_required
def delete(table_name):
  if request.method == 'GET':
    args = request.args
    field_lst = []
    for attr in tables_dict[table_name]:
        field_name = attr
        field_value = args[field_name]
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

@views.route('/update', methods=['GET', 'POST'])
@login_required
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
  
@views.route('/rename/<string:key>', methods=['GET', 'POST'])
@login_required
def rename(key):
  print(key)
  msg = ''
  if request.method == 'POST':
    new_name = request.form['name']
    print(new_name)
    print("HI")
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    print("hey 2")
    sql_query = 'alter table {0} rename {1};'.format(key, new_name)
    print("hey")
    
    try:
      cur.execute(sql_query)
      msg = 'You have successfully renamed the table !!'
      tables_dict[new_name] = tables_dict[key]
      del tables_dict[key]
      print(tables_dict)
      with open('website/tables.json', 'w') as json_file:
        json.dump(tables_dict, json_file)
      mysql.connection.commit()
      cur.close()
      return redirect('/display#' + str(new_name))
    except:
      return redirect(request.url)
  return render_template('rename.html', msg = msg, key = key, user=current_user)

@views.route('/where/<string:key>', methods =['GET', 'POST'])
@login_required
def where(key):
  print(key)
  msg = ''
  try:
    if request.method == 'POST':
      column_name = request.form['Column_Name']
      print(column_name)
      value = request.form['Value']
      print(value)
      print("HI")
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      query1 = "SELECT * FROM {0} WHERE {1} = '{2}'".format(key,column_name,value)
      print(query1)
      resultValue =cursor.execute(query1)
      # mysql.connection.commit()
      msg = 'You have successfully executed where clause on the table !!'
      # return redirect('/display#' + str(key))
      if resultValue > 0:
          userDetails = cursor.fetchall()
          print(userDetails)
          print(tables_dict[key])
          return render_template('output.html',userDetails=userDetails,cols = tables_dict[key],table = key,query = query1, user=current_user)
      else:
          msg = "No values found"
  except Exception as e:
     return 'There was an ERROR : ' + str(e) 
  return render_template('where.html', msg = msg, key = key, user=current_user)
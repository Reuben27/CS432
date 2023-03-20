from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from . import db, tables_dict, mysql, insert_tables_dict
import MySQLdb.cursors

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def transactions():
    return render_template("transactions.html", user=current_user)


@views.route('/base-admin', methods=['GET','POST'])
@login_required
def admin_work():
    return render_template("admin_work.html",user=current_user, tables_dict = tables_dict )


@views.route("/display", methods=['GET','POST'])
@login_required
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
    cursor.execute(sql_query_insert,data)
    mysql.connection.commit()
    flash('Insert successful', category='success')


  return render_template('display.html', tables_dict = tables_dict, keys=tables_dict.keys(), table_data = table_data, user = current_user) #, task_data = task_data, task_keys = task_keys)

@views.route('/delete/<string:table_name>', methods=['GET', 'POST'])
@login_required
def delete(table_name):
  if request.method == 'GET':
    args = request.args
    field_lst = []
    for attr in tables_dict[table_name]:
        field_name = "{}_{}".format(table_name,attr)
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
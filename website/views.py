from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User_issue
from .import db, tables_dict
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def transactions():
    # if request.method == 'POST':
    #     note = request.form.get('note')
    #     if len(note) < 1:
    #         flash("Note is too short!", category='error')
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash("Note added!", category='success')
    return render_template("transactions.html", user=current_user)

# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()
#     return jsonify({})


@views.route('/base-admin', methods=['GET','POST'])
@login_required
def admin_work():
<<<<<<< Updated upstream
    return render_template("admin_work.html",user=current_user, tables_dict = tables_dict )
=======
    return render_template("admin_work.html",user=current_user, tables_dict = tables_dict,usertype="Admin")

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

  return render_template('display.html', tables_dict = tables_dict, keys=tables_dict.keys(), table_data = table_data, user = current_user, msg =msg,usertype="Admin")

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
          return render_template('output.html',userDetails=userDetails,cols = tables_dict[key],table = key,query = query1, user=current_user,usertype="Admin")
      else:
          msg = "No values found"
  except Exception as e:
     return 'There was an ERROR : ' + str(e) 
  return render_template('where.html', msg = msg, key = key, user=current_user)

@views.route('/user-profile',methods=['GET','POST'])
@login_required
def profile():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql_query = "select user_name,email from Users where user_id={}".format(current_user.get_id())
    result = cursor.execute(sql_query)

    if result>0:
      user_data = list(cursor.fetchall())
    mysql.connection.commit()

    if request.method == 'POST':
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      data = []
      sql_query_insert = "Update Users Set user_name =%s,email=%s where user_id ={}".format(current_user.get_id())
      data.append(request.form["user_name"])
      data.append(request.form["email"])
      data = tuple(data)
      if(data[0] != user_data[0]["user_name"] or data[1] != user_data[0]["email"]):
        cursor.execute(sql_query_insert,data)
        msg = "Profile Updated"
        flash(msg,category="success")
        user_data[0]["user_name"] =data[0] 
        user_data[0]["email"] = data[1]
      else:
        msg = "No changes detected"
        flash(msg,category="error")
      print(msg)
      mysql.connection.commit()

    return render_template("user_profile.html",user=current_user,uname = user_data[0]["user_name"],usermail=user_data[0]["email"],usertype="User")


@views.route('/prev-trans',methods=['GET'])
@login_required
def transactions():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql_query = "select transaction_id from user_issue where user_id={}".format(current_user.get_id())
    result = cursor.execute(sql_query)

    if result>0:
      transactions = list(cursor.fetchall())
      transactionlist = []
      for i in transactions:
        transactionlist.append(i["transaction_id"])
      sql_query = "select * from transactions where transaction_id in {}".format(tuple(transactionlist))
      res = cursor.execute(sql_query)
      transaction_result = list(cursor.fetchall())

      sql_query = "select * from equip_issue where transaction_id in {}".format(tuple(transactionlist))
      res = cursor.execute(sql_query)
      equipids_result = list(cursor.fetchall())
      equpids = []
      for i in equipids_result:
        if i["equipment_id"] not in equpids:
          equpids.append(i["equipment_id"])

      sql_query = "select equipment_id, name from inventory where equipment_id in {}".format(tuple(equpids))
      res = cursor.execute(sql_query)
      if res>0:
        equipids_result = list(cursor.fetchall())
        mysql.connection.commit()
      equipments_name = {}
      for i in equipids_result:
        equipments_name[i["equipment_id"]] = i["name"]

      for i in transaction_result:
        tid = i["transaction_id"]
        for j in equipids_result:
          if j["transaction_id"] == tid:
            eqid = j["equipment_id"]
        i["name"]  = equipments_name[eqid]

    return render_template("transactions.html", user=current_user, usertype="User",utransactions = transaction_result)
    
        





    
    
>>>>>>> Stashed changes

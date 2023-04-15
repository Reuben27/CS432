from flask import Blueprint, render_template, request, flash, jsonify, redirect,url_for
from flask_login import login_required, current_user
from .import db, tables_dict, mysql
import MySQLdb.cursors
import json
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/',methods=['GET','POST'])
def index():
  return render_template("index.html",user = current_user)

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
    transactions_query = "SELECT t.transaction_id, name, issue_time, return_time, damage_status FROM transactions t INNER JOIN user_issue ui ON t.transaction_id= ui.transaction_id and ui.user_ID = {} INNER JOIN equip_issue ei ON t.transaction_id= ei.transaction_id INNER JOIN inventory i ON ei.equipment_id = i.equipment_id ".format(current_user.get_id())
    cursor.execute(transactions_query)
    transactions = list(cursor.fetchall())
    mysql.connection.commit()
    for i in transactions:
      for j in i.values():
        if j == datetime(2000,1,1,0,0,0):
          i["return_time"] = "Not Returned"
    return render_template("transactions.html", user=current_user,utransactions = transactions,usertype="User")


@views.route('/equip-issue',methods=['GET','POST'])
@login_required
def issue():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql_query = "select * from Inventory"
    cursor.execute(sql_query)
    temp = list(cursor.fetchall())
    inventory_data = {}
    for i in temp:
      inventory_data[i["name"]] = i["equipment_ID"]
    mysql.connection.commit()

    if request.method == 'POST':
      issue_time = request.form["issue_time"]
      if(issue_time == ''):
        flash("Please select date and time","error")
        return redirect(url_for("views.issue"))
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      eq_id = inventory_data[request.form["eq_name"]]
      trans_data = []
      equip_issue_data = []
      user_issue_data = []
      trans_insert = "INSERT INTO transactions(issue_time,return_time,damage_status) VALUES ( %s,%s,%s)"

      trans_data =[issue_time,"2000-01-01 00:00:00","FALSE"]
      cursor.execute(trans_insert,tuple(trans_data))

      get_id_query = "SELECT LAST_INSERT_ID() as id"
      cursor.execute(get_id_query)
      result = list(cursor.fetchall())
      trans_id = result[0]["id"]
      if (trans_id>0):
        equip_issue_data = [trans_id,eq_id,trans_id,current_user.get_id()]

        eq_issue_insert="INSERT INTO equip_issue(transaction_ID,equipment_ID) VALUES (%s,%s)"
        user_issue_insert="INSERT INTO user_issue(transaction_ID,user_ID) VALUES (%s,%s)"

        print(equip_issue_data)
        print(user_issue_data)
        try:
          cursor.execute(eq_issue_insert,tuple(equip_issue_data))
          cursor.execute(user_issue_insert,tuple(user_issue_data))
          flash("Equipment Issued with Transaction ID: "+str(trans_id),"success")

        except:
          flash("Equipment Issue Failed","error")

      else:
        flash("Equipment Issue Failed","error")

      mysql.connection.commit()
    return render_template("equip_issue.html",user=current_user, inventorydata = inventory_data,usertype="User")

@views.route('/equip-return',methods=['GET','POST'])
@login_required
def return_equip():
    fees = 0
    description = ""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    transactions_query = "select transaction_id as id from user_issue where user_id={}".format(current_user.get_id())
    result = cursor.execute(transactions_query)
    
    if(result>0):
      temp = list(cursor.fetchall())
      transactionlist = []
      for i in temp:
        transactionlist.append(i["id"])
      returntime_query = "select transaction_id as id, issue_time from transactions where return_time = '2000-01-01 00:00:00' and transaction_id in {}".format(tuple(transactionlist))

      cursor.execute(returntime_query)
      temp = list(cursor.fetchall())
      finaltransactionlist = []
      transtime ={}
      for i in temp:
        finaltransactionlist.append(i["id"])
        transtime[i["id"]] = i["issue_time"]

    if request.method == 'POST':
      try:
        trans_id = int(request.form["trans_id"])
        return_time = request.form["return_time"]
              
      except:
        flash("Please fill the values", "error")
        return redirect(url_for("views.return_equip"))

      
      issue_time = transtime[trans_id]
      
      dt_rt = datetime.strptime(return_time,'%Y-%m-%dT%H:%M')
      dt_it = issue_time
      delay = dt_rt-dt_it
      delay = delay.total_seconds()/(60*60)

      if(delay<0):
        flash("Return time invalid","error")
        return redirect("view.return_equip")
      
      else:
        if delay > 10:
          fees = 10
          description = "Late"
        damage = request.form["damage"]
        trans_data = []
        trans_data.append(return_time)
        if(damage == "TRUE"):
          fees= fees + 100
          if(description ==""):
            description = "Broken"
          else:
            description = description+ " & Broken"
          trans_data.append("TRUE")
        else:
          trans_data.append("FALSE")
        trans_data.append(trans_id)

        if fees != 0:
          penalty_query = "INSERT INTO penalty(description) VALUE (%s)"
          fee_id_query = "SELECT LAST_INSERT_ID() as id"
          cursor.execute(penalty_query,[description])
          cursor.execute(fee_id_query)
          temp = list(cursor.fetchall())
          fee_id = temp[0]["id"]
          
          strike_query = "INSERT INTO strike(transaction_ID,fee_receipt_ID,Delay,Fees) VALUES (%s,%s,%s,%s)"
          strike_data = [trans_id,fee_id,delay,fees]
          print(strike_data)
          cursor.execute(strike_query,tuple(strike_data))   
        trans_update = "UPDATE transactions SET return_time=%s, damage_status=%s where transaction_ID = %s"
        try:
          cursor.execute(trans_update,tuple(trans_data))
          
          flash("Item returned successfully","success")
        except:
          flash("Item return failed", "error")

      

    mysql.connection.commit()
    return render_template("equip_return.html",user=current_user, transactiondata = finaltransactionlist,usertype="User")









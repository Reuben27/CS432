from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Your Password'
app.config['MYSQL_DB'] = 'Your Database Name'

mysql = MySQL(app)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/practice', methods =['GET', 'POST'])
def practice():
  msg = ''
  if request.method == 'POST':
    Id = request.form['Id']
    firstname = request.form['firstname']
    roll = request.form['roll']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO practice VALUES (% s, % s, % s)',(Id, firstname, roll ))
    mysql.connection.commit()
    msg = 'You have successfully inserted the data !!'
  return render_template('practice.html', msg = msg)

if __name__ == "__main__":
  app.run(debug=True)
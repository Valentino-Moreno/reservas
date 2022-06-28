from flask import Flask, render_template, request,redirect,url_for, flash
from flask_mysqldb import MySQL

app = Flask (__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'prueba'
mysql = MySQL(app)

app.secret_key = "mysecretkey"

@app.route('/')
def Index():
    return render_template('registro.html')
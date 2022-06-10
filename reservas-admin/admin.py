import email
from flask import Flask, render_template, request,redirect,url_for, flash
from flask_mysqldb import MySQL

app = Flask (__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'prueba'
mysql = MySQL(app)

app.secret_key = "mysecretkey"


#Ruta principal
@app.route('/')
def Index():
    return render_template('principal.html')

#Inicio admin
@app.route('/verificacion_admin', methods=['GET', 'POST'])
def verificacion():
    print("llegue")
    if request.method == 'POST':
        user = request.form['admin_user']
        password = request.form['admin_password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM admin WHERE admin_user =' + '"' + user + '"' + "AND admin_password =" + '"' + password + '"')
        usuario_existente = cur.rowcount
        if usuario_existente <= 0:
            return render_template('alertaa.html')
        else:
            print("llegue")
            return render_template('perfiladmin.html')

#Crear un aula
@app.route('/add_course', methods=['POST'])
def add_course():
    if request.method == 'POST':
        course = request.form['course_name']
        capacity = request.form['course_capacity']
        pcs = request.form['pc_availables']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO course (course_name, course_capacity, pc_availables) VALUES (%s,%s,%s)", (course, capacity, pcs))
        mysql.connection.commit()
        return render_template('perfiladmin.html')



if __name__ == "__main__":
    app.run(port=3001, debug=True)
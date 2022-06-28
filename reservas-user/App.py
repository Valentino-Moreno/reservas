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
def registro():
    return render_template('registro.html')


#Registro de un profesor
@app.route('/add_user', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['teacher_name']
        user = request.form['teacher_user']
        email = request.form['teacher_email']
        password = request.form['teacher_password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM teacher WHERE teacher_user = ' + '"' + user + '"')
        usuario_existente = cur.rowcount
        cur.execute('SELECT * FROM teacher WHERE teacher_email = ' + '"' + email + '"')
        email_existente = cur.rowcount

        if usuario_existente <= 0 and email_existente <= 0:
            cur.execute("INSERT INTO teacher (teacher_name, teacher_user, teacher_email, teacher_password) VALUES (%s,%s,%s,%s)", (fullname, user, email, password))
            mysql.connection.commit()
            return redirect(url_for('login'))
        else:
            return render_template('alerta.html')

#Renderiza la plantilla del formulario de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

#Verifica los datos para hacer el login
@app.route('/verificacion', methods=['GET', 'POST'])
def verificacion():
    if request.method == 'POST':
        email = request.form['teacher_email']
        password = request.form['teacher_password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM teacher WHERE teacher_email =' + '"' + email + '"' + "AND teacher_password =" + '"' + password + '"')
        usuario_existente = cur.rowcount
        if usuario_existente <= 0:
            return render_template('alertaa.html')
        else:
            cur.execute('SELECT * FROM teacher WHERE teacher_email=' + '"' + email + '"')
            data = cur.fetchone()
            cur.execute('SELECT * FROM course')
            data2 = cur.fetchall()
            cur.execute('SELECT * FROM subject WHERE idteacher=' + '"' + str(data[0]) + '"')
            data3 = cur.fetchall()
            print(data3)
            return render_template('perfil.html', usuario = data, cursos=data2, materias=data3)

#Renderiza la plantilla con los datos de perfil 
@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    return render_template('perfil.html')

#Hacer una reserva
@app.route('/reservar', methods=['GET','POST'])
def reservar():
    cur = mysql.connection.cursor()
   
    #
    curso = request.form['idcourse']
    materia = request.form['idsubject']
    dia = request.form['reservation_date']
    hora = request.form['reservation_hour']
    cur.execute("INSERT INTO reservation(idcourse, idsubject, reservation_date, reservation_hour) VALUES(%s,%s,%s,%s)",(curso,materia,dia,hora))
    mysql.connection.commit()
    
    return render_template('perfil.html')

    
if __name__ == "__main__":
    app.run(port=3000, debug=True)
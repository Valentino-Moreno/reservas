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
    if request.method == 'POST':
        user = request.form['admin_user']
        password = request.form['admin_password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM admin WHERE admin_user =' + '"' + user + '"' + "AND admin_password =" + '"' + password + '"')
        usuario_existente = cur.rowcount
        if usuario_existente <= 0:
            return render_template('alertaa.html')
        else:
            return render_template('perfiladmin.html')
#Ir a aula+
@app.route('/irAula')
def irAula():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM course')
    data = cur.fetchall()
    print(data)
    return render_template('aulas.html', aulas = data)

#Crear un aula
@app.route('/add_course', methods=['POST', 'GET'])
def add_course():
    if request.method == 'POST':
        course = request.form['course_name']
        capacity = request.form['course_capacity']
        pcs = request.form['pc_availables']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO course (course_name, course_capacity, pc_availables) VALUES (%s,%s,%s)", (course, capacity, pcs))
        mysql.connection.commit()
        return redirect(url_for('irAula'))

#Borrar Aulas
@app.route('/deleteAula/<string:idcourse>', methods=['POST','GET'])
def deleteAula(idcourse):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM course WHERE idcourse={0}'.format(idcourse))
    mysql.connection.commit()
    return redirect(url_for('irAula'))

#Crear un materia
@app.route('/add_subject', methods=['POST', 'GET'])
def add_subject():
    if request.method == 'POST':
        materia = request.form['subject_name']
        prioridad = request.form['subject_priority']
        profesor = request.form['idteacher']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO subject (subject_name, subject_priority, idteacher) VALUES (%s,%s,%s)", (materia, prioridad, profesor))
        mysql.connection.commit()
        return redirect(url_for('irMateria'))

#Ir a materias
@app.route('/irMateria')
def irMateria():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM subject join teacher on subject.idteacher = teacher.idteacher')
    data = cur.fetchall()
    cur.execute('SELECT * FROM teacher')
    tea = cur.fetchall()
    #cur.execute('SELECT teacher_name FROM teacher T JOIN subject S ON T.idteacher = S.idteacher')
    #test =  cur.fetchall()
    print(data)
    #cur.execute("SELECT teacher_name FROM teacher WHERE idteacher = '" + profesor + '"')
    #nomb = cur.fetchall()
    return render_template('materias.html', subjects = data, profesores = tea)

#Borrar Materias
@app.route('/deleteMaterias/<string:idsubject>', methods=['POST','GET'])
def deleteMaterias(idsubject):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM subject WHERE idsubject={0}'.format(idsubject))
    mysql.connection.commit()
    return redirect(url_for('irMateria'))


if __name__ == "__main__":
    app.run(port=3001, debug=True)
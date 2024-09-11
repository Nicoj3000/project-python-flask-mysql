from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'proyectowebflask'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    sql = "SELECT * FROM equipos"
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql)
    equipos = cursor.fetchall()
    return render_template('sitio/index.html', equipos=equipos)

@app.route('/sitio/guardar', methods=['POST'])
def guardar():
    descripcion = request.form['descripcion']
    email = request.form['email']
    sql = "INSERT INTO equipos (descripcion, email) VALUES (%s, %s)"
    datos = (descripcion, email)
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    return redirect('/sitio/equipos')

@app.route('/sitio/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM equipos WHERE codigo=%s", (id,))
    conexion.commit()
    return redirect('/sitio/equipos')

@app.route('/sitio/editar/<int:id>')
def editar(id):
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM equipos WHERE codigo=%s", (id,))
    equipo = cursor.fetchone()
    return render_template('sitio/editar.html', equipo=equipo)

@app.route('/sitio/actualizar/<int:codigo>', methods=['POST'])
def actualizar(codigo):
    if request.method == 'POST':
        email = request.form['email']
        descripcion = request.form['descripcion']
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE equipos
            SET email = %s, descripcion = %s
            WHERE codigo = %s
        """, (email, descripcion, codigo))
        mysql.connection.commit()
        return redirect('/sitio/equipos')

@app.route('/sitio/equipos')
def equipos():
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM equipos")
    equipos = cursor.fetchall()
    return render_template('sitio/equipos.html', equipos=equipos)

@app.route('/sitio/usuarios')
def usuarios():
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    return render_template('sitio/usuarios.html', usuarios=usuarios)

@app.route('/sitio/guardar_usuario', methods=['POST'])
def guardar_usuario():
    username = request.form['username']
    password = request.form['password']
    sql = "INSERT INTO usuarios (username, password) VALUES (%s, %s)"
    datos = (username, password)
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    return redirect('/sitio/usuarios')

@app.route('/sitio/eliminar_usuario/<int:id>')
def eliminar_usuario(id):
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id=%s", (id,))
    conexion.commit()
    return redirect('/sitio/usuarios')

@app.route('/sitio/editar_usuario/<int:id>')
def editar_usuario(id):
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
    usuario = cursor.fetchone()
    return render_template('sitio/editar_usuario.html', usuario=usuario)

@app.route('/sitio/actualizar_usuario/<int:id>', methods=['POST'])
def actualizar_usuario(id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE usuarios
            SET username = %s, password = %s
            WHERE id = %s
        """, (username, password, id))
        mysql.connection.commit()
        return redirect('/sitio/usuarios')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, flash, redirect, request, session, url_for
from flask import render_template
from conexion import conectar

app = Flask(__name__)
app.secret_key='mi clave secreta'

@app.route('/')
def inicio():
    # print(session)
    if 'email' in session:
        email=session["email"]
        return render_template('index.html', email=email)
    return redirect(url_for('login'))
    

@app.route('/registrarse')
def registrarse():
    return render_template('registrarse.html')

@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    nombres=request.form['nombres']
    apellidos=request.form['apellidos']
    cedula=request.form['cedula']
    celular=request.form['celular']
    email=request.form['email']
    password=request.form['password']
    if nombres == '' or apellidos == '' or cedula == '' or celular == '' or email == '' or password == '':
        flash('Llene todos los campos')
        # verificamos que llene los datos del formulario
        return redirect(url_for('registrarse'))
    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE correo=%s",(email,))
        registros = cursor.fetchall()
    print(registros)
    if len(registros)>0:
        flash('El correo ya se encuentra registrado')
        #Ya esta registrado el correo
        conexion.close()
        return redirect(url_for('registrarse'))
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuarios(nombres, apellidos, celular, correo, identificacion, password, tipoUsuario) VALUES (%s, %s, %s, %s, %s, %s, 'usuario')",
                       (nombres, apellidos, celular, email, cedula, password))
    conexion.commit()
    conexion.close()

    session["email"] = email
    session["nivel"] = 'usuario'
    # print(session)
    
    
    return redirect(url_for('inicio'))

@app.route('/logout')
def logout():
    session.clear()
    print(session)
    return redirect(url_for('inicio'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/inicio_sesion', methods=['POST'])
def inicio_sesion():
    email=request.form['email']
    password=request.form['password']
    if email == '' or password == '':
        flash('Llene todos los campos')
        # verificamos que llene los datos del formulario
        return redirect(url_for('login'))
    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE correo=%s",(email,))
        registros = cursor.fetchall()
    print(registros)

    if len(registros)==0:
        flash('El correo no se encuentra registrado')
        #No esta registrado el correo
        conexion.close()
        return redirect(url_for('login'))
    
    passwd=registros[0][6]
    if password != passwd:
        flash('La contraseña es incorrecta')
        conexion.close()
        return redirect(url_for('login'))
    
    session["email"] = email
    session["nivel"] = registros[0][7]
    # print(session)
    #############Aqui se hace la validacion si es usuario o admin
    if session["nivel"]=='usuario':
        return redirect(url_for('inicio'))
    else:
        return redirect(url_for('inicio'))
        # return redirect(url_for('inicio_admin'))
    


@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/otros')
def otros():
    return render_template('otros.html')

@app.route('/patilleras')
def patilleras():
    return render_template('patilleras.html')

@app.route('/maquinas')
def maquinas():
    return render_template('maquinas.html')

@app.route('/shavers')
def shavers():
    return render_template('shavers.html')

@app.route('/capas')
def capas():
    return render_template('capas.html')

@app.route('/tijeras')
def tijeras():
    return render_template('tijeras.html')

# Manejo de excepción 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=5000,debug=True)
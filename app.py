import os #modulo de sistema op. para eliminar la foto y updatearla
from flask import Flask
from flask import render_template, request,redirect, send_from_directory, url_for, flash
 #los request son solicitud de info, redirect permite redireccionar
 #flash sirve para dar mensajes de validacion
from flaskext.mysql import MySQL
from datetime import datetime #para grabar el id de foto

#en el patron MVC flask.py funciona como Controlador
app= Flask(__name__)
app.secret_key="SecretKey"
mysql= MySQL() #creamos instancia mysql
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sysempleados'
mysql.init_app(app)

#referenciar a la carpeta donde se subiran las fotos, con la libreria os
CARPETA=os.path.join('uploads')
app.config['CARPETA']=CARPETA

#para obtener la foto desde uploads en la tabla
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

#para abrir el index vamos a la terminal : "python app.py"
@app.route("/") #indicamos la redireccion del url
def index():

    sql= "SELECT * FROM `sysempleados`.`empleados` ";
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql) #ejecutamos la sentencia sql 
    empleados= cursor.fetchall() #convierte a tupla los datos
    #print(empleados) #mostrarlo en la terminal
    conn.commit()

    return render_template('empleados/index.html', empleados=empleados)



@app.route('/destroy/<int:id>')
def destroy(id):
    conn= mysql.connect()
    cursor= conn.cursor()

    cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)
    ubicacion= cursor.fetchall() #lo convierte en tupla pero necesitamos solo la [0][0]
    os.remove(os.path.join(app.config['CARPETA'], ubicacion[0][0]))  
        
    cursor.execute("DELETE FROM `sysempleados`.`empleados` WHERE id=%s ", (id))
    conn.commit()
    return redirect('/')

@app.route('/create') #cuando llamemos a create nos redigira a ese html
def create():
    return render_template('empleados/create.html')

@app.route('/update', methods=['POST'])
def update():
    _nombre= request.form['txtNombre']
    _correo= request.form['txtCorreo']
    _foto= request.files['txtFoto']
    id= request.form['txtID']

    sql= "UPDATE `sysempleados`.`empleados` SET `nombre`=%s, `correo`=%s WHERE id=%s ;"
    datos= (_nombre, _correo, id)

    conn= mysql.connect()
    cursor= conn.cursor()
    now= datetime.now()
    tiempo= now.strftime("%Y%H%M%S") #año-hora-min-seg

  
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename 
        _foto.save("uploads/"+nuevoNombreFoto) 
        cursor.execute("SELECT foto FROM `sysempleados`.`empleados` WHERE id=%s", id) 
        fila= cursor.fetchall() 
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0])) 
        cursor.execute("UPDATE `sysempleados`.`empleados` SET foto=%s WHERE id=%s;", (nuevoNombreFoto, id)) 
        conn.commit() 

    cursor.execute(sql, datos) 
    conn.commit() 
    return redirect('/')


@app.route('/edit/<int:id>')
def edit(id):  
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM `sysempleados`.`empleados` WHERE id=%s ", (id))
    empleados= cursor.fetchall() #convierte a tupla los datos
    conn.commit()
    return render_template('empleados/edit.html', empleados=empleados)



@app.route('/store', methods=["POST"]) #redireccionamiento del form create
#aclarando que será de un metodo post
def storage():
    _nombre= request.form['txtNombre']
    _correo= request.form['txtCorreo']
    _foto= request.files['txtFoto']

    #validacion de formulario completado:
    if _nombre=='' or _correo=='' or _foto=='':
        flash("Recuerda completar todos los campos")
        return redirect(url_for('create'))

    #guardar el nombre de la foto con datetime
    now= datetime.now()
    tiempo= now.strftime("%Y%H%M%S") #año-hora-min-seg
    nuevoNombreFoto='' #TO DO TO FIX ARREGLAR PENDIENTE
    if _foto.filename!='':
        nuevoNombreFoto= tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

    sql= "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos= (_nombre, _correo, nuevoNombreFoto)
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql, datos) #ejecutamos la sentencia sql 
    conn.commit()

    return redirect('/')

#esto va al final porque es la ejecucion del programa
if __name__=='__main__':
    app.run(debug=True)
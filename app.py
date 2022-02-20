from flask import Flask
from flask import render_template, request,redirect #los request son solicitud de info, redirect permite redireccionar
from flaskext.mysql import MySQL
from datetime import datetime #para grabar el id de foto

#en el patron MVC flask.py funciona como Controlador
app= Flask(__name__)
mysql= MySQL() #creamos instancia mysql
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sysempleados'
mysql.init_app(app)


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


@app.route('/create') #cuando llamemos a create nos redigira a ese html
def create():
    return render_template('empleados/create.html')
@app.route('/destroy/<int:id>')
def destroy(id):
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute("DELETE FROM `sysempleados`.`empleados` WHERE id=%s ", (id))
    conn.commit()
    return redirect('/')

@app.route('/store', methods=["POST"]) #redireccionamiento del form create
#aclarando queserá de un metodo post
def storage():
    _nombre= request.form['txtNombre']
    _correo= request.form['txtCorreo']
    _foto= request.files['txtFoto']
    #guardar el nombre de la foto con datetime
    now= datetime.now()
    tiempo= now.strftime("%Y%H%M%S") #año-hora-min-seg
    if _foto.filename!='':
        nuevoNombreFoto= tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

    sql= "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos= (_nombre, _correo, nuevoNombreFoto)
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql, datos) #ejecutamos la sentencia sql 
    conn.commit()

    return render_template('empleados/index.html')

#esto va al final porque es la ejecucion del programa
if __name__=='__main__':
    app.run(debug=True)
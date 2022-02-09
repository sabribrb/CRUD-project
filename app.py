from venv import create
from flask import Flask
from flask import render_template, request #los request son solicitud de info
from flaskext.mysql import MySQL

#en el patron MVC flask.py funciona como Controlador
app= Flask(__name__)
mysql= MySQL() #creamos instancia mysql
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sysempleados'
mysql.init_app(app)



@app.route("/") #indicamos la redireccion del url
def index():

    sql= "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, 'Jose', 'josecarlos65@gmail.com', 'curriculum2.jpg');";
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql) #ejecutamos la sentencia sql 
    conn.commit()

    return render_template('empleados/index.html')
#para abrir el index vamos a la terminal c "python app.py"
@app.route('/create') #cuando llamemos a create nos redigira a ese html
def create():
    return render_template('empleados/create.html')
#esto va al final porque es la ejecucion del programa
if __name__=='__main__':
    app.run(debug=True)
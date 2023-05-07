from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app=Flask(__name__)

#conexión a mysql
app.config['MYSQL_HOST'] = 'localhost'          #ASIGNA SERVIDOR
app.config['MYSQL_USER'] = 'root'               #USUARIO
app.config['MYSQL_PASSWORD'] = 'root'           #CONTRASEÑA
app.config['MYSQL_DB'] = 'unadatabase'          #BASE DE DATOS
mysql = MySQL(app)

# settings                                      #inicializa una sesión
app.secret_key = '1234'                         #datos que guarda la app del servidor para después reutilizarlos(cookies, memoria del serv., memoria del navegador)


            ###  C L A S E S  ###

class Routines:
    def __init__(self, nombre):
        self.nombre = nombre
        self.exercises=[]
    
    def add_excercise(self, exercise):
        self.exercises.append(exercise)
        flash ("Ejercicio %s agregado a la rutina %s", (self.exercise, self.nombre))

    def delete_excercise(self):
        self.exercises.remove(self.exercise)


           
            ###  R U T A S  ###

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM ejercicios')
    data = cur.fetchall()
    print(data)
    return render_template('add_excercise.html', excercises = data)     #con ese segundo parámetro le paso los datos a html con el nombre exercises

@app.route('/delete/<string:id>')      #la ruta es delete y recibe un parámetro de tipo string
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM ejercicios WHERE id= {0}'.format(id))
    mysql.connection.commit()
    flash('Ejercicio removido con éxito')
    return redirect(url_for('index'))

@app.route('/edit/<id>')            #parámetro sin definir tipo de dato
def get_excercise(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM ejercicios WHERE id= %s', (id, ))    #los valores se pasan como tuplas, por eso la ',', porque sino arroja error
    data = cur.fetchall()
    return render_template('edit_excercise.html', excercise = data[0])          #retorna el template

@app.route('/update/<id>', methods = ['POST'])
def update_excercise(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        principal_muscle = request.form['principal_muscle']
        if request.form['secondary_muscle']=='':
            secondary_muscle='-'
        else:
            secondary_muscle = request.form['secondary_muscle']
        cur = mysql.connection.cursor()                             #con """ """ se puede hacer un texto en múltiples líneas
        cur.execute("""                             
            UPDATE ejercicios 
            SET nombre=%s,
            musculo_principal=%s,
            musculo_secundario=%s
            WHERE id=%s
        """, (fullname, principal_muscle, secondary_muscle, id))       
        mysql.connection.commit()     
    flash('datos actualizados')
    return redirect(url_for('index')) 

@app.route('/my_progress')
def my_progress():
    return render_template('progress.html')

@app.route('/trainings')
def my_trainings():
    return render_template('progress.html')

@app.route('/add_excercise', methods=['GET', 'POST'])
def add_excercise():
    if request.method == 'POST':                #si el método da info al servidor y no viceversa
        fullname = request.form['fullname']     #guarda lo recopilado en una variable para poder operar con el dato
        principal_muscle = request.form['principal_muscle']
        if request.form['secondary_muscle']=='':
            secondary_muscle='-'
        else:
            secondary_muscle = request.form['secondary_muscle']
        print (request.form['fullname'])        #para controlar que funciona
        cur = mysql.connection.cursor()         #conecta la bbdd para modificarla desde acá
        cur.execute('INSERT INTO ejercicios (nombre, musculo_principal, musculo_secundario) VALUES (%s, %s, %s)', (fullname, principal_muscle, secondary_muscle))   #consulta SQL
        mysql.connection.commit()               #ejecuta la consulta SQL en la bbdd
        flash('¡Ejercicio añadido con éxito!')  # Mensajes entre vistas
        return redirect(url_for('index'))                   #retorna una redirección al template


if __name__=='__main__':
    app.run(debug=True, port=5000)








# class ejercicio:
#     def __init__(self, nombre, musculoPrincipal) -> None:
#         self.nombre = nombre
#         self.musculoPrincipal = musculoPrincipal
#         self.volumenTotal=0
#         self.volumenSemanal=0
#         self.volumenDiario=0
#         pass

#     def realizarSerie(self, peso, repeticiones)->str:
#         self.volumenDiario+=peso*repeticiones
#         self.volumenSemanal+=self.volumenDiario
#         self.volumenTotal+=self.volumenDiario
#         return (f"{self.musculoPrincipal} ejercitado con {repeticiones} repeticiones con {peso} kilos")



# ej=ejercicio("Pecho plano", "Pectorales")
# ej.realizar



from flask import Flask, jsonify, request, render_template

from flask_mysqldb import MySQL

from config import config

app=Flask(__name__)

con=MySQL(app)

@app.route('/alumnos', methods=['GET'])
def listar_alumnos():
    try:
        cursor=con.connection.cursor()
        sql="select * from alumnos"
        cursor.execute(sql)
        datos=cursor.fetchall()
        listar_alumnos=[]
        for fila in datos:
            alum={'matricula':fila[0], 'nombre':fila[1],
                  'aPaterno':fila[2], 'aMaterno':fila[3],
                  'correo':fila[4]}
            listar_alumnos.append(alum)
        return jsonify({'alumnos':listar_alumnos, 'mensaje':'Lista de alumnos'})
    except Exception as ex:
        return jsonify({'mensaje':'error de conexion'})

def leer_alumno_bd(mat):
    try:
        cursor=con.connection.cursor()
        sql="select * from alumnos where matricula = {0}".format(mat)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
            alumno={'matricula':datos[0], 'nombre':datos[1],
                    'aPaterno':datos[2], 'aMaterno':datos[3],
                    'correo':datos[4]}
            return alumno
        else:
            return None
    except Exception as ex:
        raise ex
@app.route('/alumnos/<mat>', methods=['GET'])
def leer_alumno(mat):
    try:
        alumno=leer_alumno_bd(mat)
        if alumno !=None:
            return jsonify({'alumno':alumno, 'mensaje':'Alumnos encontrado','exito':True})
        else:
            return jsonify({'mensaje':'Alumno no encontrado','exito':False})
        
    except Exception as ex:
        return jsonify({'mensaje':'error de conexion {}'.format(ex)})

@app.route('/alumnos', methods=['POST'])
def registrar_alumno():
    try:
        alumno=leer_alumno_bd(request.json['matricula'])
        if alumno !=None:
            return jsonify({'mensaje':'Alumno ya existe','exito':False})
        else:
            cursor = con.connection.cursor()
            sql=""" INSERT INTO alumnos(matricula, nombre, aPaterno, aMaterno, correo) 
            VALUES({0},'{1}','{2}','{3}','{4}') """.format(request.json['matricula'],
            request.json['nombre'],request.json['aPaterno'], request.json['aMaterno'],
            request.json['correo'])
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':'Alumno registrado ', 'exito':True})
    except Exception as ex:
        return jsonify({'mensaje':'error de conexion {}'.format(ex)})

def pagina_no_encontrada(error):
    return "<h1> pagina no encontrada...</<h1>",404

if __name__=="__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
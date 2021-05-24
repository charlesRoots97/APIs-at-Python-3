from flask import Flask, jsonify, render_template, redirect, url_for, request, make_response
from app import app, mysql
import datetime
import jwt
import time

@app.route('/', methods=["GET","POST"])
def index():
    if request.method == 'GET':
        response = {'status': 'success', 'message': 'Bienvenido'}
        return jsonify(response)
    else:
        response = {'status': 'error', 'message': 'Method Not Allowed'}
        return jsonify(response)

# Another Method
@app.route('/post', methods=["POST"])
def post():
    username = str(request.json.get('username'))
    message = str(request.json.get('message'))

    if request.method == 'POST':

        try:
            if username == None or message == None:
                print(' ---- Dentro del if!')
                username = str(request.json.get('username'))
                message = str(request.json.get('message'))
        except:
            print(' ---- Ocurrió un error!')

        print(' ---- username', username)
        print(' ---- message', message)

        response = {'status': 'success', 'message': 'Echo OK!'}

        print(' ---- response',response)
        return jsonify(response)
    else:
        response = {'status': ' error', 'message': 'Method Not Allowed'}
        return jsonify(response)

@app.route('/accessToken', methods=["POST"])
def getAccessToken():
    # Obtención de datos de request esperado
    token = request.json['token']
    username = request.json['username']
    email = request.json['email']

    try:
        cursor = mysql.connection.cursor()
        query_all_clients = 'SELECT * FROM api_users_ads WHERE token = %s AND username = %s AND email = %s'
        cursor.execute(query_all_clients,(token,username,email))
        client_records = cursor.fetchall()
        cursor.close()

        if len(client_records) > 0:
            # Encriptación de datos para generar Access Token
            tokenJWT = jwt.encode({
                "username": username,
                "email":email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, 
                token, 
                algorithm='HS256')

            # print('\n')
            # print('********** SHOWING JWT **********')
            # print(tokenJWT)
            # print('********** SHOWING JWT **********')
            # print('\n')

            response= {'status':'success', 'accessToken': tokenJWT}
        else:
            response= {'status':'error', 'message': 'No existe dentro de nuestros registros'}
    except:
        print('******** Error con la query ********')
        response = {'status':'error', 'data':'Error','message':'Error con data'}
        return jsonify(response)

    finally:
        print('******* Datos leidos con exito *******')
    
    return jsonify(response)

@app.route('/validateAccessToken', methods=["POST"])
def validateAccessToken():
    accessToken = request.json['accessToken']
    token = request.json['token']

    # resuelto = jwt.decode(accessToken, token, algorithms=['HS256'])
    try:
        resuelto = jwt.decode(accessToken, token, algorithms=["HS256"])    

        if request.method == 'POST':
            try:
                cursor = mysql.connection.cursor()
                query = ("SELECT "+
                "tbl_productos.descripcion AS producto_descripcion, "+
                "tbl_sucursales.idsucursales AS sucursal_id, "+
                "tbl_sucursales.nombreSuc AS sucursal_nombre, "+
                "SUBSTRING(tbl_solicitud.fecha_captura,1,4) AS anio, "+
                "SUBSTRING(tbl_solicitud.fecha_captura,6,2) AS mes, "+
                "SUBSTRING(tbl_solicitud.fecha_captura,9,2) AS dia, "+
                "tbl_empleados.id_promotor AS promotor_id, "+
                "CONCAT_WS(' ', tbl_empleados.nombre_promotor, tbl_empleados.apaterno_promotor, tbl_empleados.amaterno_promotor) AS promotor_name "+
                "FROM tbl_cordinacion "+
                "INNER JOIN tbl_empresa ON tbl_empresa.id_empresa = tbl_cordinacion.fk_empresa "+
                "INNER JOIN tbl_productos ON tbl_productos.fk_empresa = tbl_empresa.id_empresa "+
                "INNER JOIN tbl_solicitud ON tbl_solicitud.fk_producto = tbl_productos.id_producto "+
                "INNER JOIN tbl_empleados ON tbl_empleados.id_promotor = tbl_solicitud.fk_promotor "+
                "INNER JOIN tbl_sucursales ON tbl_sucursales.idsucursales = tbl_empleados.fk_sucursales "+
                "WHERE tbl_empresa.id_empresa = 1 LIMIT 10")
                # query_all_users ='SELECT * FROM tbl_empleados LIMIT 1'
                cursor.execute(query)
                records = cursor.fetchall()
                cursor.close()

                # print('****************************')
                # print(' **** solicitud_records: ****', records)
                # print('****************************')

                data = []
                i = 0
                for record in records:
                    i = i+1
                    json_data = {'producto_descripcion': record['producto_descripcion'], 
                    'sucursal_id': record['sucursal_id'], 
                    'sucursal_nombre': record['sucursal_nombre'], 
                    'anio': record['anio'], 
                    'mes': record['mes'],
                    'dia': record['dia'],
                    'promotor_id': record['promotor_id'],
                    'promotor_name': record['promotor_name'],
                    'count': i,
                    'consultas': record['consultas']}
                    data.append(json_data)
            except:
                print('******** Error con la query ********')
                response = {'status':'error', 'data':'Error','message':'Error con data'}
                return jsonify(response)
            finally:
                print('******* Datos leidos con exito *******')
            
            response= {'status':'success', 'data': data}
            return jsonify(response)
        else:
            response = {'http_code':'405', 'status': 'error', 'message': 'Method Not Allowed'}
            return jsonify(response)

    except jwt.ExpiredSignatureError:
        response = {'message':'El Token ha expirado'}
    
    return jsonify(response)

@app.route('/queries', methods=['POST'])
def getQueries():
    if request.method == 'POST':
        try:
            cursor = mysql.connection.cursor()
            query_all_clients = 'SELECT * FROM api_clients_salesforce'
            cursor.execute(query_all_clients)
            client_records = cursor.fetchall()
            cursor.close()

            print('****************************')
            print(' **** client_records ****', client_records)
            print('****************************')

            append_clients = []
            for client in client_records:
                json_clients = {'clave_client': client['clave_cliente'], 'apellido_paterno': client['apellido_paterno']}
                append_clients.append(json_clients)
        except:
            print('******** Error con la query ********')
            response = {'status':'error', 'data':'Error','message':'Error con data'}
            return jsonify(response)

        finally:
            print('******* Datos leidos con exito *******')
        
        response = {'status':'success', 'data': append_clients, 'message': 'Datos de clientes'}
        return jsonify(response)

    else:
        response = {'status':'error','data':'None','message':'Method Not Allowed'}

@app.route('/jsonify', methods=['POST'])
def jsonifyMethod():

    if request.method == 'POST':
        user_data = request.json.get('user_data')
        print(' ******** user_data',user_data)
        name = str(user_data.get('name'))
        date_born = user_data.get('date_born')
        # print(' ********* name',name)
        response = {'name':name,'date_born':date_born}
        return jsonify(response)
    else:
        response = {'status':'error','message':'Method Not Allowed'}
        return jsonify(response)

@app.route('/query-users', methods=['GET'])
def getUsers():
    if request.method == 'GET':
        try:
            cursor = mysql.connection.cursor()
            query_all_users = 'SELECT * FROM tbl_usuario'
            cursor.execute(query_all_users)
            user_records = cursor.fetchall()
            cursor.close()

            print('****************************')
            print(' **** user_records: ****', user_records)
            print('****************************')

            append_users = []
            for user in user_records:
                json_users = {'id_usuario': user['id_usuario'], 'nombre': user['nombre'], 'apaterno': user['apaterno'], 'amaterno': user['amaterno'], 'email': user['email']}
                append_users.append(json_users)
        except:
            print('******** Error con la query ********')
            response = {'status':'error', 'data':'Error','message':'Error con data'}
            return jsonify(response)
        finally:
            print('******* Datos leidos con exito *******')
        
        response= {'status':'success', 'data': append_users, 'message': 'Datos de clientes'}
        return jsonify(response)
    else:
        response = {'http_code':'405', 'status': 'error', 'message': 'Method Not Allowed'}
        return jsonify(response)

@app.route('/myDB', methods=['POST'])
def queryMyDB():
    try:
        cursor = mysql.connection.cursor()
        query_all_users = 'SELECT * FROM activations INNER JOIN numbers ON activations.numbers_id = numbers.id'
        cursor.execute(query_all_users)
        user_records = cursor.fetchall()
        cursor.close()

        print('****************************')
        print(' **** user_records: ****', user_records)
        print('****************************')

        append_users = user_records
        # for user in user_records:
        #     json_users = {user}
        #     append_users.append(json_users)
    except:
        print('******** Error con la query ********')
        response = {'status':'error', 'data':'Error','message':'Error con data'}
        return jsonify(response)
    finally:
        print('******* Datos leidos con exito *******')
    
    response= {'status':'success', 'data': append_users, 'message': 'Datos de clientes'}
    return jsonify(response)
    # return jsonify({"success":"Bienvenido"})

@app.route('/queryAC', methods=['POST'])
def queryAC():
    if request.method == 'POST':
        try:
            cursor = mysql.connection.cursor()
            query = ("SELECT "+
            "tbl_productos.descripcion AS producto_descripcion, "+
            "tbl_sucursales.idsucursales AS sucursal_id, "+
            "tbl_sucursales.nombreSuc AS sucursal_nombre, "+
            "SUBSTRING(tbl_solicitud.fecha_captura,1,4) AS anio, "+
            "SUBSTRING(tbl_solicitud.fecha_captura,6,2) AS mes, "+
            "SUBSTRING(tbl_solicitud.fecha_captura,9,2) AS dia, "+
            "tbl_empleados.id_promotor AS promotor_id, "+
            "CONCAT_WS(' ', tbl_empleados.nombre_promotor, tbl_empleados.apaterno_promotor, tbl_empleados.amaterno_promotor) AS promotor_name "+
            "FROM tbl_cordinacion "+
            "INNER JOIN tbl_empresa ON tbl_empresa.id_empresa = tbl_cordinacion.fk_empresa "+
            "INNER JOIN tbl_productos ON tbl_productos.fk_empresa = tbl_empresa.id_empresa "+
            "INNER JOIN tbl_solicitud ON tbl_solicitud.fk_producto = tbl_productos.id_producto "+
            "INNER JOIN tbl_empleados ON tbl_empleados.id_promotor = tbl_solicitud.fk_promotor "+
            "INNER JOIN tbl_sucursales ON tbl_sucursales.idsucursales = tbl_empleados.fk_sucursales "+
            "WHERE tbl_empresa.id_empresa = 1 LIMIT 1000")
            # query_all_users ='SELECT * FROM tbl_empleados LIMIT 1'
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()

            # print('****************************')
            # print(' **** solicitud_records: ****', records)
            # print('****************************')

            data = []
            i = 0
            for record in records:
                i = i+1
                json_data = {'producto_descripcion': record['producto_descripcion'], 
                'sucursal_id': record['sucursal_id'], 
                'sucursal_nombre': record['sucursal_nombre'], 
                'anio': record['anio'], 
                'mes': record['mes'],
                'dia': record['dia'],
                'promotor_id': record['promotor_id'],
                'promotor_name': record['promotor_name'],
                'count': i}
                data.append(json_data)
        except:
            print('******** Error con la query ********')
            response = {'status':'error', 'data':'Error','message':'Error con data'}
            return jsonify(response)
        finally:
            print('******* Datos leidos con exito *******')
        
        response= {'status':'success', 'data': data}
        return jsonify(response)
    else:
        response = {'http_code':'405', 'status': 'error', 'message': 'Method Not Allowed'}
        return jsonify(response)
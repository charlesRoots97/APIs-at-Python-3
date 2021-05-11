from flask import Flask, jsonify, render_template, redirect, url_for, request, make_response
from app import app, mysql
import datetime
import jwt
import time

@app.route('/', methods=["GET","POST"])
def index():
    if request.method == 'GET':
        response = {'status': ' success', 'message': 'Bienvenido'}
        return jsonify(response)
    else:
        response = {'status': ' error', 'message': 'Method Not Allowed'}
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
            format = "%Y-%m-%d %H:%M:%S"
            today = datetime.datetime.today()
            today = today.strftime(format)
            ts = int(time.time())

            # Encriptación de datos para generar Access Token
            tokenJWT = jwt.encode({
                "username": username,
                "email":email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)}, 
                token, 
                algorithm='HS256')

            print('\n')
            print('********** SHOWING JWT **********')
            print(tokenJWT)
            print('********** SHOWING JWT **********')
            print('\n')

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
        
        response= {'status':'success', 'data': append_clients, 'message': 'Datos de clientes'}
        return jsonify(response)

    else:
        reponse = {'status':'error','data':'None','message':'Method Not Allowed'}

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

@app.route('/token', methods=['POST'])
def create_token():
    username = request.json.get('username',None)
    password = request.json.get('password',None)

    return jsonify({'user': username, 'pass': password})
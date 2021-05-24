import routes
from app import app

HOST = '127.0.0.1'
PORT = 5000

# from modulos.gantt.blueprint import mod_gantt

# app.register_blueprint(mod_gantt, url_prefix='/modulos/gantt')

if __name__ == '__main__':
   app.run(host=HOST, port=PORT)
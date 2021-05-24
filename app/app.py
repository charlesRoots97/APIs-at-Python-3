from flask_mysqldb import MySQL
from flask import Flask
from config import Configuration

TEST_HOST = 'corporativoads19.dyndns.org'
TEST_PORT = '2794'
TEST_USER = 'jaguar'
TEST_PASS = 'jaguar2021'
TEST_DB_NAME = 'a20191903_sigce2'

# TEST_HOST = 'localhost'
# TEST_PORT = '3306'
# TEST_USER = 'root'
# TEST_PASS = ''
# TEST_DB_NAME = 'crm'

app = Flask(__name__)
app.config.from_object(Configuration)

app.config['MYSQL_HOST'] = TEST_HOST
app.config['MYSQL_PORT'] = int(TEST_PORT)
app.config['MYSQL_DB'] = TEST_DB_NAME
app.config['MYSQL_USER'] = TEST_USER
app.config['MYSQL_PASSWORD'] = TEST_PASS
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
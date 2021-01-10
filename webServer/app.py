from flask import Flask, render_template, jsonify, request
from flaskext.mysql import MySQL
import threading
import requests
app = Flask(__name__)

mysql = MySQL()
#MYSQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'lighter_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

def sql_select_sticker():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select * from STICKER_DEVICE limit 5;')
    data = cursor.fetchall()
    conn.close()
    return data

def sql_select_gas():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select * from GAS_DEVICE limit 5;')
    data = cursor.fetchall()
    conn.close()
    return data

def sql_select_device():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select * from SPEC_DEVICE limit 5;')
    data = cursor.fetchall()
    conn.close()
    return data


# @app.route('/led', methods=['GET'])
# def led():
#     a = request.args.get('input', 0, type=int)
#     if a == 0:
#         requests.get('http://210.94.181.91:8080/led/ON')
#     else :
#         requests.get('http://210.94.181.91:8080/led/OFF')
#     return 'SUCCESS'

# @app.route('/NodeMCU', methods=['GET', 'POST'])
# def test():
#     print ("NODEMCU CONNECTED!!!!!!!")
#     value = request.data.decode('utf-8')
#     print ("MESSAGE : " + value)
#     return "Connection Successed!"

# @app.route('/getAirCondition', methods=['GET'])
# def getAirCondition():
#     return requests.get('http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?sidoName=%EC%84%9C%EC%9A%B8&pageNo=1&numOfRows=10&ServiceKey=' + api_service_key + '&ver=1.3&_returnType=json').json()


@app.route('/getSticker', methods=['GET'])
def getSticker():
    data = sql_select_sticker()
    return jsonify(data)

@app.route('/getGas', methods=['GET'])
def getGas():
    data = sql_select_gas()
    return jsonify(data)

@app.route('/getDevice', methods=['GET'])
def getDevice():
    data = sql_select_device()
    return jsonify(data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

from flask import Flask, render_template, jsonify, request
from flaskext.mysql import MySQL
import threading
import requests
app = Flask(__name__)

mysql = MySQL()
#MYSQL configurations
app.config['MYSQL_DATABASE_USER'] = 'choi'
app.config['MYSQL_DATABASE_PASSWORD'] = 'chOicha0'
app.config['MYSQL_DATABASE_DB'] = 'iotProject'
app.config['MYSQL_DATABASE_HOST'] = '3.133.139.175'
api_service_key = 'rTgkWoe%2FDfnKVsvwwiN8fT%2B6Sw7aiOMWaWH7YGczxqvnTHINnvTMv6PEHqA72S0ra3lAmKDtBhBcGxFisdD1ig%3D%3D'

mysql.init_app(app)
def sql_select():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select * from iotProject.tbl_sensor_temp order by sensor_id DESC limit 5;')
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/led', methods=['GET'])
def led():
    a = request.args.get('input', 0, type=int)
    if a == 0:
        requests.get('http://210.94.181.91:8080/led/ON')
    else :
        requests.get('http://210.94.181.91:8080/led/OFF')
    return 'SUCCESS'

@app.route('/getAirCondition', methods=['GET'])
def getAirCondition():
    return requests.get('http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?sidoName=%EC%84%9C%EC%9A%B8&pageNo=1&numOfRows=10&ServiceKey=' + api_service_key + '&ver=1.3&_returnType=json').json()
    

@app.route('/getData', methods=['GET'])
def getData():
    data = sql_select()
    return jsonify(data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

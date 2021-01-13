from flask import Flask, render_template, jsonify, request
from flaskext.mysql import MySQL
import threading
import requests
from PIL import Image
import base64
import io
import PIL.Image

app = Flask(__name__)

mysql = MySQL()
#MYSQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'lighter_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql.init_app(app)

loc = 'STICKER_DEVICE'
loc2 = 'GAS_DEVICE'

def sql_select_sticker():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select create_at, device_id, state, image_path from STICKER_DEVICE ORDER BY create_at DESC limit 5;')
    data = cursor.fetchall()
    conn.close()
    return data

def sql_select_gas():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select create_at, device_id, state, image_path from GAS_DEVICE ORDER BY create_at DESC limit 5;')
    data = cursor.fetchall()
    conn.close()
    return data

def sql_select_device():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select * from SPEC_DEVICE ORDER BY create_at DESC limit 5;')
    data = cursor.fetchall()
    conn.close()
    return data

def sql_select_img(loc):
    conn = mysql.connect()
    cursor = conn.cursor()
    SQLStatement2 = "SELECT image_file FROM {0} ORDER BY create_at DESC LIMIT 1"
    cursor.execute(SQLStatement2.format(loc))
    result = cursor.fetchone()[0] # image 1개
    data = io.BytesIO(result)
    # img=PIL.Image.open(io.BytesIO(result[0]))
    StoreFilePath = "C:\\Users\\user10\\Desktop\\lighter\\code\\homepage\\lighter_homepage\\webServer\\static\\image\\img{0}.jpg".format(id)
    print(StoreFilePath)
    with open(StoreFilePath, "wb") as File:
        File.write(result)
        File.close()
    return 'image/img{0}.jpg'.format(id)

# def sql_select_img(loc2):
#     conn = mysql.connect()
#     cursor = conn.cursor()
#     SQLStatement2 = "SELECT image_file FROM {0} ORDER BY create_at DESC LIMIT 1"
#     cursor.execute(SQLStatement2.format(loc2))
#     result = cursor.fetchone()[0] # image 1개
#     data = io.BytesIO(result)
#     # img=PIL.Image.open(io.BytesIO(result[0]))
#     StoreFilePath = "C:\\Users\\user10\\Desktop\\lighter\\code\\homepage\\lighter_homepage\\webServer\\static\\image\\img{0}.jpg".format(id)
#     print(StoreFilePath)
#     with open(StoreFilePath, "wb") as File:
#         File.write(result)
#         File.close()
#     return 'image/img{0}.jpg'.format(id)


@app.route('/update', methods=['GET'])
def update():
    a = request.args.get('input', 0, type=int)
    if a == 0:
        requests.get('url/update/ON')
    else :
        requests.get('url/update/OFF')
    return 'SUCCESS'

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

@app.route('/getImage', methods=['GET'])
def getImage():
    StoreFilePath = sql_select_img(loc)
    return StoreFilePath

@app.route('/')
def index():
    sql_select_sticker()
    return render_template('index.html')
    # return render_template('index.html', image_file = sql_select_img(loc) , img_data = getImage())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

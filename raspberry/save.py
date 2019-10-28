import time
import Adafruit_DHT
import threading
import RPi.GPIO as GPIO
from flask import Flask, render_template
from flaskext.mysql import MySQL

app = Flask(__name__)       # for flask
sensor = Adafruit_DHT.DHT11 # DHT11 init
pin_temp = 4                
pin_led = 17
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_led, GPIO.OUT)

mysql = MySQL()
#MYSQL configurations
app.config['MYSQL_DATABASE_USER'] = 'choi'
app.config['MYSQL_DATABASE_PASSWORD'] = 'chOicha0'
app.config['MYSQL_DATABASE_DB'] = 'iotProject'
app.config['MYSQL_DATABASE_HOST'] = '3.133.139.175'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

def saveData():
    try:
        while True:
            # 1. Get Data from sensor
            h, t = Adafruit_DHT.read_retry(sensor, pin_temp)
            if h is not None and t is not None :
                print("Temperature = {0:0.1f}*C Humidity = {1:0.1f}%".format(t, h))
            else :
                print('Read error')
            # 2. Store Data in mysql
            cursor.callproc('store_temp_val', (t, h, 'MY_SENSOR'))
            data = cursor.fetchall()
            # 3. check for error
            if len(data) is 0:
                conn.commit()
                print ('data stroed successfully!')
            else :
                print ('error occur' + data[0])
            # 4. sleep for 5 minute
            time.sleep(5 * 60)  
    except KeyboardInterrupt:
        return


@app.route('/led/<status>', methods=['GET'])
def changeLED(status):
    if status == 'ON':
        GPIO.output(pin_led, True)
        time.sleep(0.1)
    else :
        GPIO.output(pin_led, False)
        time.sleep(0.1)

if __name__ == '__main__':
    t1 = threading.Thread(target=saveData)
    t1.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
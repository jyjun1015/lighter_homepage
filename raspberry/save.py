from flask import Flask, render_template
from flaskext.mysql import MySQL
import threading
app = Flask(__name__)

mysql = MySQL()
#MYSQL configurations
app.config['MYSQL_DATABASE_USER'] = 'choi'
app.config['MYSQL_DATABASE_PASSWORD'] = 'chOicha0'
app.config['MYSQL_DATABASE_DB'] = 'iotProject'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

def saveData():
    cursor.callproc('store_temp_val', (20.5, 60.5))
    data = cursor.fetchall()
    if len(data) is 0:
        conn.commit()
        print ('data stroed successfully!')
    else :
        print ('error occur' + data[0])


@app.route('/')
def index():
    cursor.execute('select * from iotProject.tbl_sensor_temp order by sensor_id DESC limit 5;')
    data = cursor.fetchall()
    return render_template('index.html', results = data)


if __name__ == '__main__':
    t1 = threading.Thread(target=saveData)
    t1.start()
    app.run()
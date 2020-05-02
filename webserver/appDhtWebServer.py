from flask import Flask, render_template, request
import os

app = Flask(__name__)
import sqlite3
# Retrieve data from database
def getData():
    conn=sqlite3.connect('/home/pi/Desktop/Projekt/sqlite/db/baza.db')
    curs=conn.cursor()
    for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
        time = str(row[0])
        temp = row[1]
        hum = row[2]
    conn.close()
    return time, temp, hum

#Create list of images and return newest
def getLatest():
    arr = os.listdir("/home/pi/Desktop/Projekt/dhtWebServer/static/cam")
    arr.sort()
    return "static/cam/" + arr[-1]

# main route
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/dhtdata")
def dhtdata():
    latest_img = getLatest()
    time, temp, hum = getData()
    templateData = {
        'time': time,
        'temp': temp,
        'hum': hum,
        'latest_img':latest_img
    }
    return render_template('dhtdata.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=4081, debug=False, threaded=True)

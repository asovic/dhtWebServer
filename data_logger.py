import time
import sqlite3
import Adafruit_DHT
import datetime

database = "/home/pi/Desktop/Projekt/sqlite/db/baza.db"
sampleFreq = 30

def GetData():
    sensor = Adafruit_DHT.DHT22
    pin = 4
    temp, hum = Adafruit_DHT.read_retry(sensor,pin)
    #if hum is not None and temp is not None:
    if hum <= 100.0 and hum >= 0.0 and temp <= 100.0 and temp >= -50.0:
        hum = round(hum,1)
        temp = round(temp,1)
        return hum,temp
#        else:
#            print('Bad reading at {}'.format(datetime.datetime.now()))

def LogData(temp,hum):
    conn = sqlite3.connect(database)
    curs = conn.cursor()
    curs.execute("INSERT INTO DHT_data values(datetime('now', '2 hours'), (?), (?))", (temp, hum))
    conn.commit()
    conn.close()

def main():
    while True:
        temp, hum = GetData()
        if hum <= 100.0 and hum >= 0.0 and temp <= 100.0 and temp >= -50.0:
            LogData(temp, hum)
        else:
            print('Bad reading at {}'.format(datetime.datetime.now()))
        time.sleep(sampleFreq)
main()
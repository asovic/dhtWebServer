import sqlite3
import time
import datetime
import matplotlib
matplotlib.use('Agg')
from dateutil import parser
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import threading

plt.rcParams.update({'figure.max_open_warning': 0})

def graph_data():
    database = '/home/pi/Desktop/Projekt/sqlite/db/baza.db'
    conn = sqlite3.connect(database)
    c = conn.cursor()
    
    sql = "SELECT * FROM DHT_data ORDER BY timestamp"
    c.execute(sql)
    data = c.fetchall()
    
    temperature = []
    humidity = []
    timeframe = []
    
    for row in data:
        temperature.append(row[1])
        humidity.append(row[2])
        timeframe.append(parser.parse(row[0]))
        
#    for t in temperature:
#        if t == 'Bad reading':
#            i = temperature.index(t)
#            temperature.pop(i)
#    for h in humidity:
#        if h == 'Bad reading':
#            i = humidity.index(h)
#            humidity.pop(i)
            
    dates = [matplotlib.dates.date2num(t) for t in timeframe]
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_title('Sensor data')
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H:%M'))
    ax1.set_ylabel('Temperature [C]')
    ax1.plot_date(dates, temperature, '-', label='Temperature', color='r')
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('Rel. humidity [% RH]')
    ax2.plot_date(dates, humidity, '-', label='Humidity', color='b')
    
    fig.autofmt_xdate(rotation=60)
    fig.tight_layout()
    
    ax1.grid(True)
    ax1.legend(loc='lower left', framealpha=0.5)
    ax2.legend(loc='lower right', framealpha=0.5)
    
    plt.savefig('/home/pi/Desktop/Projekt/dhtWebServer/static/figure.png')
    plt.close()
    c.close()
    conn.close()

def main():
    while True:
        graph_data()
        time.sleep(300)
main()

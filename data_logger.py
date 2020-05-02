from time import sleep
import sqlite3
import Adafruit_DHT
import datetime
import math
import numpy
import threading

database = "/home/pi/Desktop/Projekt/sqlite/db/baza.db"
sampleFreq = 30

filtered_temperature = [] # here we keep the temperature values after removing outliers
filtered_humidity = [] # here we keep the filtered humidity values after removing the outliers

lock = threading.Lock() # we are using locks so we don't have conflicts while accessing the shared variables
event = threading.Event() # we are using an event so we can close the thread as soon as KeyboardInterrupt is raised

# function which eliminates the noise
# by using a statistical model
# we determine the standard normal deviation and we exclude anything that goes beyond a threshold
# think of a probability distribution plot - we remove the extremes
# the greater the std_factor, the more "forgiving" is the algorithm with the extreme values
def eliminateNoise(values, std_factor = 2):
    mean = numpy.mean(values)
    standard_deviation = numpy.std(values)

    if standard_deviation == 0:
        return values

    final_values = [element for element in values if element > mean - std_factor * standard_deviation]
    final_values = [element for element in final_values if element < mean + std_factor * standard_deviation]

    return final_values

# function for processing the data
# filtering, periods of time, yada yada
def readingValues():
    values = []
    sensor = Adafruit_DHT.DHT22
    pin = 4
    
    while not event.is_set():
        counter = 0
        while counter < sampleFreq and not event.is_set():
            temp = None
            humidity = None
            try:
                [humidity, temp] = Adafruit_DHT.read_retry(sensor,pin)

            except IOError:
                print("we've got IO error")

            if math.isnan(temp) == False and math.isnan(humidity) == False:
                values.append({"temp" : temp, "hum" : humidity})
                counter += 1
            #else:
                #print("we've got NaN")

            sleep(1)

        lock.acquire()
        filtered_temperature.append(numpy.mean(eliminateNoise([x["temp"] for x in values])))
        filtered_humidity.append(numpy.mean(eliminateNoise([x["hum"] for x in values])))
        lock.release()

        values = []

#def GetData():
#    sensor = Adafruit_DHT.DHT22
#    pin = 4
#    temp, hum = Adafruit_DHT.read_retry(sensor,pin)
#    if hum is not None and temp is not None:
#        hum = round(hum,1)
#        temp = round(temp,1)
#        return hum,temp
#    else:
#        print('Bad reading at {}'.format(datetime.datetime.now()))

def LogData(temp,hum):
    conn = sqlite3.connect(database)
    curs = conn.cursor()
    curs.execute("INSERT INTO DHT_data values(datetime('now', '2 hours'), (?), (?))", (temp, hum))
    conn.commit()
    conn.close()

def Main():
    data_collector = threading.Thread(target = readingValues)
    data_collector.start()
    
    while not event.is_set():
        if len(filtered_temperature) > 0: # or we could have used filtered_humidity instead
            lock.acquire()
            
            temp = round(filtered_temperature.pop(), 1)
            hum = round(filtered_humidity.pop(), 1)
            
            LogData(temp, hum)
            lock.release()
        sleep(1)
    data_collector.join()
    
if __name__ == "__main__":
    try:
        Main()

    except KeyboardInterrupt:
        event.set()

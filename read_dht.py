import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
pin = '4'



def read_sensor():
    hum, temp = Adafruit_DHT.read_retry(sensor, pin)
    if hum is not None and temp is not None:
        hum = round(hum, 1)
        temp = round(temp, 1)
        return temp,hum
    else:
        print('Coulnt get a reading.')
read_sensor()
import RPi.GPIO as GPIO
import time, sys, os
import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085
import time
import requests
import math
import random


TOKEN = "A1E-dAXdHlkUh5QGMSs1XZDNpiuzby3zAc"  # Put your TOKEN here
DEVICE_LABEL = "trab"  # Put your device label here 
VARIABLE_LABEL_1 = "temperatura"  # Put your first variable label here
VARIABLE_LABEL_2 = "umidade"
VARIABLE_LABEL_3 = "pressao"
VARIABLE_LABEL_4 = "atuador"
atuador = True

sensor2 = BMP085.BMP085()
sensor = Adafruit_DHT.DHT11
gpio = 4
humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
DELAY = 2  # Delay in seconds



GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT) #RGB blue
GPIO.output(17,0)
GPIO.setup(27,GPIO.OUT) #RGB green
GPIO.output(27,0)
GPIO.setup(22,GPIO.OUT) #RGB red
GPIO.output(22,0)




def build_payload(variable_1, variable_2, variable_3):
    # Creates two random values for sending data
    value_1 = temperature
    value_2 = humidity
    value_3 = format(sensor2.read_pressure())
    payload = {variable_1: value_1,
               variable_2: value_2,
               variable_3: value_3 }

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://things.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():




    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')
    if (atuador==1):
        if temperature < 20:
            GPIO.output(17,GPIO.HIGH)
        elif temperature > 27:
            GPIO.output(22,GPIO.HIGH)
        elif (temperature>20 and temperature < 27):
            GPIO.output(27,GPIO.HIGH)
    else:
        GPIO.output(17,0)
        GPIO.output(22,0)
        GPIO.output(27,0)

    print('Pressure = {0:0.2f} Pa'.format(sensor2.read_pressure()))
    payload = build_payload(VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")

def get_var(device, variable):
    try:
        url = "http://things.ubidots.com/"
        url = url + \
            "api/v1.6/devices/{0}/{1}/".format(device, variable)
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        req = requests.get(url=url, headers=headers)
        return req.json()['last_value']['value']
    except:
        pass


if __name__ == '__main__':
    while (True):
        main()
        atuador = get_var(DEVICE_LABEL, VARIABLE_LABEL_4)
        print(atuador)
        time.sleep(5)








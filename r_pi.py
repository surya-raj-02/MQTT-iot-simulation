import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

mqttBroker = "test.mosquitto.org"
client = mqtt.Client("rasp_pi")
client.connect(mqttBroker)

print("Connected to MQTT server!!!")

topic_list = [
    "iot-assignemnt-sss-ultra-sensor", "iot-assignemnt-sss-force-sensor",
    "iot-assignemnt-sss-gas-sensor", "iot-assignemnt-sss-motion-sensor"
]

while True:
    randNumber = uniform(20.0, 21.0)
    client.publish("TEMPERATURE", randNumber)
    print("Just published " + str(randNumber) + " to topic TEMPERATURE")
    time.sleep(1)
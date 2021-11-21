from os import read
import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
import csv

mqttBroker = "test.mosquitto.org"
client = mqtt.Client("rasp_pi")
client.connect(mqttBroker)

print("Connected to MQTT server!!!")

topic = [
    "iot-assignment-sss/ultra-sensor", "iot-assignment-sss/force-sensor",
    "iot-assignment-sss/gas-sensor", "iot-assignment-sss/motion-sensor"
]
topic1 = "iot-assignment-sss/onehot"

flag = int(input("Select '1' for sending data manually and '2' for sending through file:"))
if flag == 1:
    while True:
        data_to_be_sent = input("Enter one hot encoded values in order: ultrasonic, force, gas, motion:")
        client.publish(topic1,data_to_be_sent)
        print("Just published " + str(data_to_be_sent) + " to topic " + topic1)
        time.sleep(1)
elif flag == 2:
    loc = input("Enter file location:")
    if loc == "":
        loc = "example.csv"
    with open(loc) as f:
        reader = csv.reader(f)
        data = list(reader)
    for i in data:
        client.publish(topic[0],i[0])
        client.publish(topic[1],i[1])
        client.publish(topic[2],i[2])
        client.publish(topic[3],i[3])
        client.publish(topic1,i[4])
        print("published:", i)
        time.sleep(3)
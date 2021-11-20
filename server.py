import paho.mqtt.client as mqtt
import time
import os



def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))


def on_message2(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

def on_message3(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))


mqttBroker ="test.mosquitto.org"

client = mqtt.Client("Server1")
print("Connected to MQTT server!!!")


client.connect(mqttBroker)
client.loop_start()
client.subscribe("iot-assignemnt-sss/#")

client.message_callback_add("iot-assignemnt-sss/ultra-sensor", on_message)
client.message_callback_add("iot-assignemnt-sss/force-sensor", on_message2)
client.message_callback_add("iot-assignemnt-sss", on_message3)


time.sleep(300)
client.loop_stop()
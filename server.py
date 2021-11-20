import paho.mqtt.client as mqtt
import time
import os
from flask import Flask, request, render_template
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder='templates')
app.config['DEBUG'] = True



def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))
    @app.route('/print_it', methods=['POST', 'GET'])
    def print_it():
        print("received message: " ,str(message.payload.decode("utf-8")))
        return render_template('index.html', message=str(message.payload.decode("utf-8")))
    return print_it()


def on_message2(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))
    @app.route('/print_it2', methods=['POST', 'GET'])
    def print_it():
        print("received message: " ,str(message.payload.decode("utf-8")))
        return render_template('index.html', message=str(message.payload.decode("utf-8")))
    return print_it()

mqttBroker ="test.mosquitto.org"

client = mqtt.Client("Server1")
client.connect(mqttBroker) 

print("Connected to MQTT server!!!")

client.loop_start()

client.message_callback_add("iot-assignemnt-sss/ultra-sensor", on_message)
client.message_callback_add("iot-assignemnt-sss/force-sensor", on_message2)
client.connect(mqttBroker)
client.subscribe("iot-assignemnt-sss/#")
time.sleep(30)
client.loop_stop()
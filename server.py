from csv import excel
import paho.mqtt.client as mqtt
import time
import os
import threading

# # Basic blask server to catch events
from flask import Flask, render_template
from flask_socketio import SocketIO, emit


def t2(indata):
    app = Flask(__name__)
    socketio = SocketIO(app, async_mode='threading')
    
    def task1():
            while 1:
                try:
                    msg = indata.pop()
                    print(msg)
                    socketio.emit("send message", {"data": msg})
                    print("EMITED")
                    time.sleep(2)
                except:
                    time.sleep(2)

    @socketio.on('got_message')
    def test_message(message):  # test_message() is the event callback function.
        print(message)
        emit('my response',{'data': message})  # Trigger a new event called "my response"
        print("msg sent")
        # that can be caught by another callback later in the program.

    @app.route('/')
    def index():
        
        x = threading.Thread(target=task1)
        x.start()
        return render_template('index.html')
    
    socketio.run(app)


def t1(putdata):
    def on_message(client, userdata, message):
        print("received message: " ,str(message.payload.decode("utf-8")))
        putdata.append(str(message.payload.decode("utf-8")))
        print(putdata)

    # def on_message2(client, userdata, message):
    #     print("received message: ", str(message.payload.decode("utf-8")))

    # def on_message3(client, userdata, message):
    #     print("received message: ", str(message.payload.decode("utf-8")))

    mqttBroker = "test.mosquitto.org"

    client = mqtt.Client("Server1")

    client.connect(mqttBroker)
    print("Connected to MQTT server!!!")
    client.loop_start()
    client.subscribe("iot-assignment-sss")
    client.on_message = on_message

    # client.message_callback_add("iot-assignemnt-sss/ultra-sensor", on_message)
    # client.message_callback_add("iot-assignemnt-sss/force-sensor", on_message2)
    # client.message_callback_add("iot-assignemnt-sss", on_message3)

    time.sleep(300)
    client.loop_stop()


if __name__ == '__main__':
    q = []
    t11 = threading.Thread(target=t1, args=(q,))
    t22 = threading.Thread(target=t2, args=(q,))

    t11.start()
    t22.start()
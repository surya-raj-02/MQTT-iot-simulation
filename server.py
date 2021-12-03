import signal
async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

from csv import excel
from logging import debug
import paho.mqtt.client as mqtt
import time
import os
import threading

# # Basic blask server to catch events
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
thread = None


# @socketio.on('send message', namespace="/test")
# def test_message(message):  # test_message() is the event callback function.
#     print(message)
#     emit('my response',
#          {'data': message})  # Trigger a new event called "my response"
#     print("msg sent")
#     # that can be caught by another callback later in the program.


@app.route('/')
def index():

    global thread
    if thread is None:
        thread = threading.Thread(target=t1)
        thread.daemon = True
        thread.start()
    return render_template('index.html')


def t1():
    topic = [
        "iot-assignment-sss/ultra-sensor", "iot-assignment-sss/force-sensor",
        "iot-assignment-sss/gas-sensor", "iot-assignment-sss/motion-sensor","iot-assignment-sss/onehot"
    ]

    def on_message(client, userdata, message):
        if message.topic == "iot-assignment-sss/ultra-sensor":
            socketio.emit("send ultra",
                      {"data": str(message.payload.decode("utf-8"))},
                      namespace="/test")
            fp.write("ultra:"+str(message.payload.decode("utf-8"))+"\n")
        elif message.topic == "iot-assignment-sss/force-sensor":
            socketio.emit("send force",
                      {"data": str(message.payload.decode("utf-8"))},
                      namespace="/test")
            fp.write("force:"+str(message.payload.decode("utf-8"))+"\n")
        elif message.topic == "iot-assignment-sss/gas-sensor":
            socketio.emit("send gas",
                      {"data": str(message.payload.decode("utf-8"))},
                      namespace="/test")
            fp.write("gas:"+str(message.payload.decode("utf-8"))+"\n")
        elif message.topic == "iot-assignment-sss/motion-sensor":
            socketio.emit("send motion",
                      {"data": str(message.payload.decode("utf-8"))},
                      namespace="/test")
            fp.write("motion:"+str(message.payload.decode("utf-8"))+"\n")
        elif message.topic == "iot-assignment-sss/onehot":
            socketio.emit("send one-hot",
                      {"data": str(message.payload.decode("utf-8"))},
                      namespace="/test")
            fp.write("onehot:"+str(message.payload.decode("utf-8"))+"\n")
        print(str(message.payload.decode("utf-8")))

    def on_connect(client, userdata, flags, rc):
        for i in topic:
            client.subscribe(i)

    # def on_message2(client, userdata, message):
    #     print("received message: ", str(message.payload.decode("utf-8")))

    # def on_message3(client, userdata, message):
    #     print("received message: ", str(message.payload.decode("utf-8")))
    mqttBroker = "test.mosquitto.org"

    client = mqtt.Client("Server1")

    client.connect(mqttBroker)
    print("Connected to MQTT server!!!")
    client.on_connect = on_connect
    client.loop_start()
    client.on_message = on_message

    time.sleep(300)
    client.loop_stop()


if __name__ == '__main__':
    global fp
    fp = open("serv_data.csv","a")
    def handler(signum, frame):
            fp.close()
            exit(1)
    signal.signal(signal.SIGINT, handler)
    socketio.run(app, debug=True)
    # socketio.run(app, debug=True, host="192.168.1.39")
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

@socketio.on('send message',namespace="/test")
def test_message(
        message):  # test_message() is the event callback function.
    print(message)
    emit('my response',
            {'data': message})  # Trigger a new event called "my response"
    print("msg sent")
    # that can be caught by another callback later in the program.

@app.route('/')
def index():

    global thread
    if thread is None:
        thread = threading.Thread(target=t1)
        thread.daemon = True
        thread.start()
    return render_template('index.html')



def t1():
    def on_message(client, userdata, message):
        print("received message: ", str(message.payload.decode("utf-8")))
        socketio.emit("send message", {"data": str(message.payload.decode("utf-8"))}, namespace="/test")
        print("emitted ig")

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
    socketio.run(app)
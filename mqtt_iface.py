import paho.mqtt.client as mqtt
import time
import random
import socket


# user = 'User_1'
# _passwrd = 'P@$$w0Rd'

hosts = [
    '192.168.xxx.xxx',
    'core-mosquitto',
    'mqtt.eclipse.org'
]
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)


# The callback for when the client receives a response.
def on_connect(client, userdata, flags, results):
    # 0: Connection successful
    # 1: Connection refused - incorrect protocol version
    # 2: Connection refused - invalid client identifier
    # 3: Connection refused - server unavailable
    # 4: Connection refused - bad username or password
    # 5: Connection refused - not authorised
    # 6 - 255: Currently unused.
    print("Connected with result code " + str(results))

    # renewed subscriptions on reconnect.
    # client.subscribe("someTopic")


# The callback for when a message is received.
def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


class MQTT:

    def __init__(self, host_, client_id=None, _user=None, _paswrd=None):
        self.client = mqtt.Client(
            client_id=client_id,
            clean_session=True,
        )
        # set callback for connection
        self.client.on_connect = on_connect
        # set callback for received message
        self.client.on_message = on_message

        # set credentials
        self.client.username_pw_set(username=_user, password=_paswrd)

        self.client.connect(
            host=host_,  # dev-pi-b address
            port=2121,  # dev port
        )

    def sub(self, _topic):
        self.client.subscribe(_topic)

    def pub(self, _topic, msg=''):
        self.client.publish(_topic, msg)

    def start(self):
        try:  # run
            self.pub(publish_to)
            while self.client:  # start
                self.client.loop_forever(
                    # timeout=60,
                    # retry_first_connection=True
                )
        finally:  # clean up
            self.client.loop_stop()
            self.client.disconnect()

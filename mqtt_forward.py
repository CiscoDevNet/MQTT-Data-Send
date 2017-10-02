from minio import Minio
import ast
import paho.mqtt.client as mqtt
import time
import datetime

minio = "minio"
minio_conn = True

while minio_conn:
    try:
        minioClient = Minio('%s:9000' % minio,
                            access_key="AKIAIOSFODNN7EXAMPLE",
                            secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                            secure=False)
        minio_conn = False
    except Exception:
        pass

data = minioClient.get_object("mqtt", "mqtt_config.json")
string_conf = data.read().decode()
print(string_conf)
mqtt_config = ast.literal_eval(string_conf)
mqtt_broker = mqtt_config["mqtt_ip"]

msg_frq = mqtt_config["msg_per_sec"]
msg_data = mqtt_config["msg_data"]
alt_msg_data = mqtt_config["alt_msg_data"]
msg_str = str(msg_data)
alt_msg_str = str(alt_msg_data)


def on_publish(client, userdata, mid):
    print(msg_str)


client = mqtt.Client()
client.on_publish = on_publish
client.connect(mqtt_broker, 1883)
client.loop_start()


if mqtt_config["checkbox"] == "on":
    while True:
        ts = time.time()
        dt = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        (rc, mid) = client.publish("IOx", str(msg_str + ", " + dt))
        time.sleep(mqtt_config["msg_per_sec"])
        (rc, mid) = client.publish("IOx", str(alt_msg_str + ", " + dt))
        time.sleep(mqtt_config["msg_per_sec"])
else:
    while True:
        ts = time.time()
        dt = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        (rc, mid) = client.publish("IOx", str(msg_str + ", " + dt))
        time.sleep(mqtt_config["msg_per_sec"])

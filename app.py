from flask import Flask, request, render_template
from minio import Minio
import io
import docker
import os

app = Flask(__name__)

MINIO_ACCESS_KEY = os.getenv("AKIAIOSFODNN7EXAMPLE")
MINIO_SECRET_KEY = os.getenv("wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY")

"""minioClient = Minio('play.minio.io:9000',
                    access_key="Q3AM3UQ867SPQQA43P2F",
                    secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
                    secure=True)"""

docker_client = docker.from_env()


@app.route("/", methods=["GET"])
def index():
    if request.args.get('MQTT IP'):
        mqtt = request.args.get('MQTT IP')
        msg_per_sec = float(request.args.get('msg per second'))
        msg_data = request.args.get('message data')
        checkbox = request.args.get('alt-data')
        alt_msg_data = request.args.get('alt message data')

        mqtt_config = str({'mqtt_ip': mqtt,
                           'msg_per_sec': msg_per_sec,
                           'msg_data': msg_data,
                           'checkbox': checkbox,
                           'alt_msg_data': alt_msg_data})

        minioClient = Minio('minio:9000',
                            access_key=MINIO_ACCESS_KEY,
                            secret_key=MINIO_SECRET_KEY,
                            secure=False)

        if minioClient.bucket_exists("mqtt"):
            minioClient.remove_bucket("mqtt")
        else:
            minioClient.make_bucket("mqtt")

        mqtt_conf_io = io.BytesIO(mqtt_config.encode())
        io_len = len(mqtt_config)
        minioClient.put_object("mqtt", "mqtt_config.json", mqtt_conf_io, io_len)

        if docker_client.get("mqtt_forward"):
            mqtt_fwd_service = docker_client.containers.get("mqtt_forward")
            mqtt_fwd_service.remove()
            docker_client.create("mqtt_forward:latest",
                                 detach=True,
                                 name="mqtt_forward",
                                 networks="data-svc",
                                 restart_policy="Always")
        else:
            docker_client.create("mqtt_forward:latest",
                                 detach=True,
                                 name="mqtt_forward",
                                 networks="data-svc",
                                 restart_policy="Always")

        return render_template("index.html")
    else:
        return render_template("index.html")

    # return render_template("index.html")


if __name__ == "__main__":
    app.run(port=5656, debug=True)

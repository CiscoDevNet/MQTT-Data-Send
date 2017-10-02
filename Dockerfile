FROM python:alpine

RUN apk update

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY mqtt_forward.py .

CMD ["python", "minio-test.py"]
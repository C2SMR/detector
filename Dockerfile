FROM python:3.10

WORKDIR /app
COPY src /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r requirements.txt

CMD python3 -u main.py ${ROBOFLOW_VERSION} ${RASPBERRY_KEY}
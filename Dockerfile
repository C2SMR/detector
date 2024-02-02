FROM python:3.10

WORKDIR /app
COPY src /app

RUN apt-get update && apt-get install -y libglib2.0-0 libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

CMD python3 -u main.py ${ROBOFLOW_VERSION} ${RASPBERRY_KEY} ${MYSQL_HOST} ${MYSQL_USER} ${MYSQL_PASSWORD} ${MYSQL_PORT} ${DETECOTR_ID}
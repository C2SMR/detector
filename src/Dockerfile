FROM python:3.10

WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python3 app.py ${LATITUDE} ${LONGITUDE} ${CITY} ${TYPE_OF_VIDEO}
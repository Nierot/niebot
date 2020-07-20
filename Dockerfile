FROM python:3.8.3

COPY . /niebot
WORKDIR /niebot

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean

RUN apt-get -y install ffmpeg

RUN python -m pip install -r requirements.txt

CMD ["python3", "main.py"]
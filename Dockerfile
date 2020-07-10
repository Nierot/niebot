FROM python:3.8.3

COPY . /niebot
WORKDIR /niebot

RUN ./get_env.sh

RUN python -m pip install -r requirements.txt

CMD ["python", "main.py"]
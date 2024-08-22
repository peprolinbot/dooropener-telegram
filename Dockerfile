FROM python:3.11

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

RUN rm /requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]
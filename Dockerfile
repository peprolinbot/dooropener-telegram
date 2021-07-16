FROM balenalib/rpi-raspbian:latest  

RUN apt-get -q update && \  
    apt-get -qy install \
        python3 python3-pip python3-dev \
        gcc make \
        python3-pygame \
        openssl

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install setuptools

RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]
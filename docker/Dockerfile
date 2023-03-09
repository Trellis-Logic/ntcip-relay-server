FROM python:3.10-bullseye

WORKDIR /usr

RUN apt-get update
RUN apt-get install python3 python3-pip libsnmp-dev -y

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY src ./src

RUN cd src && python3 setup.py install

COPY src/tests ./src/tests

CMD ["ntcip-relay-server"]

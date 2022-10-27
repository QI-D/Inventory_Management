FROM ubuntu:18.04

LABEL maintainer="qdang6@bcit.ca"

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip

COPY ./requirements.txt /storage/requirements.txt

WORKDIR /storage
RUN pip3 install -r requirements.txt
COPY . /storage

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]

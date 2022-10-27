FROM ubuntu:18.04

LABEL maintainer="qdang6@bcit.ca"

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip

COPY ./requirements.txt /receiver/requirements.txt

WORKDIR /receiver
RUN pip3 install -r requirements.txt
COPY . /receiver

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]

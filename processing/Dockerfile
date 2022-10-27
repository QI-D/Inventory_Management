FROM ubuntu:18.04

LABEL maintainer="qdang6@bcit.ca"

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip

COPY ./requirements.txt /processing/requirements.txt

WORKDIR /processing
RUN pip3 install -r requirements.txt
COPY . /processing
RUN python3 create_table.py

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]

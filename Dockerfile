FROM ubuntu:bionic

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    rtmpdump \
    ffmpeg \
    libavcodec-extra57 \
    swftools \
    python3 \
    python3-pip \
    python3-setuptools \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY . /code

RUN pip3 install wheel
RUN pip3 install -r requirements.txt
RUN python3 setup.py install

WORKDIR /app

ENTRYPOINT ["infoqscraper"]
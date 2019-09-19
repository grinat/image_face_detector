# Source:
# https://github.com/ageitgey/face_recognition/blob/a9dd28d5f97e2b5d83791548eeb9c24a807bca73/Dockerfile
# https://github.com/ageitgey/face_recognition/blob/a9dd28d5f97e2b5d83791548eeb9c24a807bca73/Dockerfile.gpu

FROM python:3.6-slim-stretch

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    make \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . ./

RUN make unittest

CMD ["make", "prod"]

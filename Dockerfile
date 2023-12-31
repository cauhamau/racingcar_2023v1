FROM nvidia/cuda:11.1-cudnn8-runtime-ubuntu18.04

RUN apt-get -y update

RUN apt-get install -y git \
    software-properties-common \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    apt install python3.6 -y && \
    apt install python3-distutils -y && \
    apt install python3.6-dev -y && \
    apt install build-essential -y && \
    apt-get install python3-pip -y && \
    apt update && apt install -y libsm6 libxext6 ffmpeg && \
    apt-get install -y libxrender-dev


COPY . /Car

RUN cd Car && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install --pre torch torchvision -f https://download.pytorch.org/whl/nightly/cu111/torch_nightly.html -U && \
    python3 -m pip install -r requirements.txt

WORKDIR /Car

CMD ["python3","./client.py"]

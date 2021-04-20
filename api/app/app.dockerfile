FROM tiangolo/uwsgi-nginx-flask:python3.6


ENV STATIC_PATH /app/app/static

COPY . /app

WORKDIR /app/app

RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt 
RUN pip install torch==1.8.1+cpu torchvision==0.9.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
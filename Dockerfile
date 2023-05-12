FROM python:3.8-slim-buster

WORKDIR /docker_demo

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

ADD . .

RUN pip install -r /docker_demo/requirements.txt

CMD ["python", "app.py"]
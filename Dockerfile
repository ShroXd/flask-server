FROM python:3.6

ADD . /code
WORKDIR /code

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . .

CMD ["gunicorn", "run:app", "-c", "./gunicorn.conf.py"]
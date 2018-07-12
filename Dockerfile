FROM python:3.6
MAINTAINER Conner Swann "me@connerswann.me"

COPY requirements.txt /tmp/requirements.txt
WORKDIR /tmp
RUN pip install -r requirements.txt
COPY app.py /app/app.py
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["app.py"]
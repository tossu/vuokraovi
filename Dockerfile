FROM python:3.5-slim

WORKDIR /opt

COPY requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

COPY src/ /opt

CMD ["python", "/opt/main.py"]

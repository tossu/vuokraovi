FROM python:3.5-slim

WORKDIR /opt

COPY requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

COPY scrapers.py /opt/scrapers.py
COPY vuokraovi.py /opt/vuokraovi.py

CMD ["python", "/opt/vuokraovi.py"]

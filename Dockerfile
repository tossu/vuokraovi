FROM python:3.5-slim

WORKDIR /opt

COPY requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

COPY apartment.py /opt/apartment.py
COPY search.py /opt/search.py
COPY vuokraovi.py /opt/vuokraovi.py

CMD ["python", "/opt/vuokraovi.py"]

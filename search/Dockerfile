FROM python:3.8-slim

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY search.py search.py
EXPOSE 9000
CMD [ "python", "./search.py" ]

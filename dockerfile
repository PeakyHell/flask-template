FROM python:3.13.0-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV FLASK_APP=website/__init__.py

RUN flask init-db

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
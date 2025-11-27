FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY food_tracker.py .

COPY templates ./templates

RUN mkdir -p /data

ENV PORT=8080

CMD ["python", "food_tracker.py"]
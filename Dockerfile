FROM python:3.12-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /app/rushim
CMD ["scrapy", "crawl", "rushim"]


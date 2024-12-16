FROM python:3.11-slim

WORKDIR /app

COPY requirements-news_web_for_docker.txt /app

RUN pip install --no-cache-dir --upgrade -r requirements-news_web_for_docker.txt

# COPY requirements.txt /app

# RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY news_web/* /app/
COPY . .

EXPOSE 5000

# CMD ["python", "/app/app.py"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"] 
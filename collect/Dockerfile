FROM python:3.13.3-slim
WORKDIR /app
COPY collect.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "collect.py"]
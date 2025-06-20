FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential\
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit","run", "dashboard/streamlit_app.py","--server.port=8501"]
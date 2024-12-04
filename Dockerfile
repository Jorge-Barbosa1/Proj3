FROM python:3.12-slim

# Instalar dependências (audio e PDF)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1-dev \
    && apt-get clean

WORKDIR /app

COPY . /app

# Instalar os requirements
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "testv2.py", "--server.port=8501", "--server.address=0.0.0.0"]

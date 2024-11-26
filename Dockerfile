FROM python:3.12-slim

# Instalar dependências do sistema (como FFmpeg)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1-dev \
    && apt-get clean

# Configurar o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do programa para o container
COPY . /app

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que o Streamlit usará
EXPOSE 8501

# Comando para rodar o programa
CMD ["streamlit", "run", "testv2.py", "--server.port=8501", "--server.address=0.0.0.0"]
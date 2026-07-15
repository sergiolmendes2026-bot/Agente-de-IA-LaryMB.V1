# Usa uma imagem oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependência primeiro para otimizar o cache
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta que o Streamlit usa
EXPOSE 8501

# Comando para iniciar o Streamlit
CMD ["streamlit", "run", "/app/dsa_assitente.py", "--server.port=8501", "--server.address=0.0.0.0"]

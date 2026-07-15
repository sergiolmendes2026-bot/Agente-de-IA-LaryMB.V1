FROM python:3.9-slim

# Define a pasta de trabalho como /app
WORKDIR /app

# Copia os requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia TUDO da raiz do repositório para a pasta /app
COPY . /app

# FORÇA o Streamlit a procurar na pasta /app
EXPOSE 8501
CMD ["streamlit", "run", "/app/dsa_assitente.py", "--server.port=8501", "--server.address=0.0.0.0"]

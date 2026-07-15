FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Vamos usar o caminho absoluto e garantir que não há erros de digitação
# Se o comando abaixo falhar, é porque o ficheiro tem um nome diferente no GitHub
CMD ["python", "-m", "streamlit", "run", "dsa_assitente.py", "--server.port=8501", "--server.address=0.0.0.0"]

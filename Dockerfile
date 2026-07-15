FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Comando de "debug": Lista os arquivos e trava o container
# Isso vai parar o erro do Streamlit e nos mostrar o que tem na pasta
CMD ["/bin/sh", "-c", "ls -R /app && sleep 3600"]

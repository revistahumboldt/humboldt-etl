# Dockerfile
# Use uma imagem base oficial do Google Cloud Functions para Python 3.9
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de dependências e os instala
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# Copia o código da sua função
COPY main.py .

# Define o ponto de entrada da função
# Para Cloud Functions, o Google Cloud espera que você defina a função a ser chamada.
# Isso geralmente é tratado pela gcloud CLI ao implantar, mas em um Dockerfile
# para um serviço Cloud Run puro, você definiria algo como:
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:hello_http"]
# No entanto, para Cloud Functions, o Cloud Buildpacks ou a CLI faz a magia por trás.
# Este Dockerfile é mais para uma "pré-visualização" do ambiente de uma função.
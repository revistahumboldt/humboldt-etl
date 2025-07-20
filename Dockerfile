# Dockerfile

# Use uma imagem base oficial do Python 3.11 (slim-buster é bom para tamanho reduzido)
FROM python:3.11-slim-buster

# Define o diretório de trabalho dentro do contêiner
# Todos os comandos subsequentes serão executados a partir deste diretório
WORKDIR /app

# Copia o arquivo de dependências (requirements.txt) e o instala
# Fazemos isso primeiro para aproveitar o cache do Docker.
# Se requirements.txt não mudar, esta camada não será reconstruída.
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# Copia todo o código da sua aplicação para o diretório de trabalho /app
# O '.' no final significa "copiar tudo do diretório atual (local) para o WORKDIR (contêiner)"
# Isso incluirá main.py, src/, utils/, .env (se estiver na raiz local)
COPY . .

# Define o comando que será executado quando o contêiner iniciar
# Como main.py está na raiz do seu projeto e você copiou a pasta 'src' para /app,
# o caminho para o seu script principal dentro do contêiner será /app/src/main.py.
CMD ["python", "src/main.py"]

# Observações:
# - Não é necessário configurar portas (como 8080) ou Gunicorn para um Cloud Run Job,
#   pois ele não serve tráfego HTTP, apenas executa um processo.
# - Para variáveis de ambiente sensíveis, use o Secret Manager do Google Cloud
#   em vez de incluí-las diretamente no Dockerfile ou no .env dentro da imagem
#   (embora para desenvolvimento inicial, o .env possa ser copiado).
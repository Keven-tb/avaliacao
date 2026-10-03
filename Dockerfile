# Usa uma imagem oficial do Python, versão slim para ser mais leve
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o arquivo de dependências primeiro
COPY app/requirements.txt .

# Instala as dependências, sem guardar cache para economizar espaço
RUN pip3 install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY app/ .

# Exponha a porta 5000 conforme o requisito
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python3", "app.py"]

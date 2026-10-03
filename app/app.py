import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Variáveis de ambiente para identificar a instância e seus vizinhos
APP_NAME = os.getenv("APP_NAME", "app_default")
PEERS = os.getenv("PEERS", "").split(",")

# Caminho do volume compartilhado
DATA_DIR = "/data"
LOG_FILE = f"{DATA_DIR}/{APP_NAME}.log"

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "JSON inválido. Falta a chave 'message'"}), 400

    message = data['message']
    
    # Flag para saber se a mensagem original veio do usuário ou de outro container
    is_replica = data.get('is_replica', False)

    # 1. Armazena localmente no próprio arquivo de log dentro do volume compartilhado
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps({"message": message}) + "\n")

    # 2. Se a mensagem veio de fora (não é réplica), envia para os outros containers
    if not is_replica:
        for peer in PEERS:
            if peer.strip():  # Ignora strings vazias
                try:
                    # Envia para o peer na porta interna (5000)
                    requests.post(
                        f"http://{peer}:5000/send", 
                        json={"message": message, "is_replica": True}, 
                        timeout=2
                    )
                except requests.exceptions.RequestException as e:
                    print(f"Erro ao replicar para {peer}: {e}")

    return jsonify({"status": "Mensagem salva", "app": APP_NAME}), 201

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            for line in f:
                if line.strip():
                    messages.append(json.loads(line.strip()))
                    
    return jsonify({"app": APP_NAME, "messages": messages}), 200

if __name__ == '__main__':
    # Ouve em todas as interfaces para funcionar dentro do Docker
    app.run(host='0.0.0.0', port=5000)

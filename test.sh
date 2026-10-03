#!/bin/bash
echo "1. A enviar mensagem 'hello' para o app1 (porta 5001)..."
curl -X POST -H "Content-Type: application/json" -d '{"message":"hello"}' http://localhost:5001/send

echo -e "\n\nA aguardar 2 segundos para a replicação..."
sleep 2

echo -e "\n2. A verificar as mensagens replicadas no app2 (porta 5002)..."
curl http://localhost:5002/messages

echo -e "\n\n3. A verificar as mensagens replicadas no app3 (porta 5003)..."
curl http://localhost:5003/messages
echo -e "\n"

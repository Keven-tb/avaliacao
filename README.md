```markdown
# Sistema de Mensagens Distribuído

Este projeto implementa um sistema de mensagens distribuído usando Python (Flask) e Docker. Múltiplos containers trocam mensagens entre si de forma automatizada e as armazenam de forma persistente em um volume compartilhado.

## Estrutura do Projeto

O projeto segue estritamente a estrutura solicitada na avaliação:

```text
/avaliacao/
├── app/
│   ├── app.py               # Código principal (API REST)
│   ├── requirements.txt     # Dependências (apenas Flask e requests)
│   └── Dockerfile           # Imagem enxuta, expondo a porta 5000
├── docker-compose.yml       # Orquestração (3 instâncias, rede bridge, volume partilhado)
├── test.sh                  # Script automatizado de teste de replicação
└── README.md                # Instruções de execução
```

## Como Executar e Exemplo de Funcionamento

1. Abra o terminal na raiz do projeto (`/avaliacao/`).
2. Levante os 3 containers em background:
```bash
# Nota: Em versões mais recentes do Docker, use 'docker compose' (sem hífen)
sudo docker-compose up -d --build
```


3. Envie uma mensagem para a instância 1 (porta 5001):
```bash
curl -X POST -H "Content-Type: application/json" -d '{"message":"hello"}' http://localhost:5001/send
```


4. Verifique se a mensagem foi replicada corretamente consultando a instância 2 (porta 5002):
```bash
curl http://localhost:5002/messages
```



## Script Automatizado de Testes

Para facilitar a validação de todos os requisitos (envio, replicação para os outros 2 containers e persistência no volume), use o script de teste.

Execute no terminal:

```bash
./test.sh
```

## Detalhes da Implementação (Arquitetura)

* **Prevenção de Loops:** O envio via POST utiliza uma flag interna (`is_replica`) para garantir que os containers não fiquem reenviando mensagens entre si infinitamente.
* **Isolamento de Logs:** Cada container mantém o seu próprio arquivo de log (`app1.log`, `app2.log`, `app3.log`) de forma individualizada dentro do diretório `/data` (que aponta para o volume compartilhado do Docker).
* **Rede e DNS:** A comunicação entre os containers usa os nomes dos serviços definidos no compose (`app1`, `app2`, `app3`) graças ao servidor de DNS ativado pela rede bridge personalizada (`rede_mensagens`).
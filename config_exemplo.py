# Configurações de conexão do banco de dados MySQL (Aiven)
# Altere estas credenciais conforme necessário

DB_CONFIG = {
    'host': 'ifmachado-agabodiwsmo-2086.g.aivencloud.com',
    'port': 16023,
    'user': 'avnadmin',
    'password': '', # Substitua pela senha real
    'database': 'defaultdb',
    'ssl_ca': 'ca.pem' # O arquivo ca.pem deve estar na mesma pasta que o main.py
}

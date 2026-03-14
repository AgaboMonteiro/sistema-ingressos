# Sistema de Ingressos (Terminal Python + MySQL)

Este é um sistema de gerenciamento de ingressos desenvolvido em Python seguindo os princípios de Programação Orientada a Objetos (POO).

## Funcionalidades
- **Login e Autenticação**: Validação de usuários.
- **CRUD de Usuários**: Cadastro e listagem.
- **CRUD de Ingressos**: Gerenciamento de eventos e estoque.
- **Venda de Ingressos**: Registro de compras com atualização automática de estoque.
- **Relatórios Top 10**: 
  - Maiores públicos (eventos mais vendidos).
  - Maiores compradores (usuários que mais gastaram).

## Requisitos
- Python 3.11+
- MySQL Server
- Bibliotecas Python: `mysql-connector-python`, `tabulate`

## Instalação
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure seu banco de dados no arquivo `config.py`:
   ```python
   DB_CONFIG = {
       'host': 'seu_host',
       'user': 'seu_usuario',
       'password': 'sua_senha',
       'database': 'sistema_ingressos'
   }
   ```

3. Execute o sistema:
   ```bash
   python main.py
   ```

## Usuário Administrador Padrão
Ao iniciar pela primeira vez (e após configurar o banco), o sistema criará automaticamente um administrador:
- **Email:** `admin@sistema.com`
- **Senha:** `admin123`

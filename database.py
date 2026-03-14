import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        try:
            if self.connection is None or not self.connection.is_connected():
                # Conexão corrigida: Removido ssl_mode (causador do erro)
                # Adicionado ssl_ca para validação segura com Aiven
                self.connection = mysql.connector.connect(
                    host=DB_CONFIG['host'],
                    port=DB_CONFIG['port'],
                    user=DB_CONFIG['user'],
                    password=DB_CONFIG['password'],
                    database=DB_CONFIG['database'],
                    ssl_ca=DB_CONFIG.get('ssl_ca'), # O caminho para o ca.pem
                    ssl_disabled=False # Garante que SSL esteja habilitado
                )
                self.create_tables()
            return self.connection
        except Error as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {e}")

    def create_tables(self):
        if not self.connection: return
        cursor = self.connection.cursor()
        
        # Tabela Usuario
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                senha VARCHAR(100) NOT NULL,
                tipo ENUM('admin', 'cliente') DEFAULT 'cliente'
            )
        """)

        # Tabela Ingresso
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingresso (
                id INT AUTO_INCREMENT PRIMARY KEY,
                evento VARCHAR(150) NOT NULL,
                preco DECIMAL(10, 2) NOT NULL,
                quantidade_disponivel INT NOT NULL,
                data_evento DATETIME NOT NULL
            )
        """)

        # Tabela CompraIngresso
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS compra_ingresso (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                ingresso_id INT NOT NULL,
                quantidade INT NOT NULL,
                valor_total DECIMAL(10, 2) NOT NULL,
                data_compra DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE,
                FOREIGN KEY (ingresso_id) REFERENCES ingresso(id) ON DELETE CASCADE
            )
        """)
        
        # Inserir um admin padrão se não existir nenhum usuário
        cursor.execute("SELECT COUNT(*) FROM usuario")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO usuario (nome, email, senha, tipo) VALUES (%s, %s, %s, %s)", 
                          ('Administrador', 'admin@sistema.com', 'admin123', 'admin'))
            self.connection.commit()

        cursor.close()

    def get_cursor(self, dictionary=True):
        try:
            conn = self.connect()
            if conn:
                return conn.cursor(dictionary=dictionary)
        except Exception as e:
            raise e
        return None

    def commit(self):
        if self.connection:
            self.connection.commit()

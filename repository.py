from database import Database
from models import Usuario, Ingresso, CompraIngresso


class BaseRepository:
    def __init__(self):
        self.db = Database()


class UsuarioRepository(BaseRepository):
    def create(self, usuario: Usuario):
        cursor = self.db.get_cursor(dictionary=False)
        if not cursor: return None
        query = "INSERT INTO usuario (nome, email, senha, tipo) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (usuario.nome, usuario.email, usuario.senha, usuario.tipo))
        self.db.commit()
        usuario.id = cursor.lastrowid
        cursor.close()
        return usuario

    def find_all(self):
        cursor = self.db.get_cursor()
        if not cursor: return []
        cursor.execute("SELECT * FROM usuario")
        rows = cursor.fetchall()
        cursor.close()
        return [Usuario(**row) for row in rows]

    def find_by_email(self, email: str):
        cursor = self.db.get_cursor()
        if not cursor: return None
        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        row = cursor.fetchone()
        cursor.close()
        return Usuario(**row) if row else None

    def find_by_id(self, id: int):
        cursor = self.db.get_cursor()
        if not cursor: return None
        cursor.execute("SELECT * FROM usuario WHERE id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()
        return Usuario(**row) if row else None

    def update(self, usuario: Usuario):
        cursor = self.db.get_cursor(dictionary=False)
        if not cursor: return False
        query = "UPDATE usuario SET nome=%s, email=%s, senha=%s, tipo=%s WHERE id=%s"
        cursor.execute(query, (usuario.nome, usuario.email, usuario.senha, usuario.tipo, usuario.id))
        self.db.commit()
        cursor.close()
        return True

    def delete(self, id: int):
        cursor = self.db.get_cursor(dictionary=False)
        if not cursor: return False
        cursor.execute("DELETE FROM usuario WHERE id = %s", (id,))
        self.db.commit()
        cursor.close()
        return True


class IngressoRepository(BaseRepository):
    def create(self, ingresso: Ingresso):
        cursor = self.db.get_cursor(dictionary=False)
        if not cursor: return None
        query = "INSERT INTO ingresso (evento, preco, quantidade_disponivel, data_evento) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (ingresso.evento, ingresso.preco, ingresso.quantidade_disponivel, ingresso.data_evento))
        self.db.commit()
        ingresso.id = cursor.lastrowid
        cursor.close()
        return ingresso

    def find_all(self):
        cursor = self.db.get_cursor()
        if not cursor: return []
        cursor.execute("SELECT * FROM ingresso")
        rows = cursor.fetchall()
        cursor.close()
        return [Ingresso(**row) for row in rows]

    def find_by_id(self, id: int):
        cursor = self.db.get_cursor()
        if not cursor: return None
        cursor.execute("SELECT * FROM ingresso WHERE id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()
        return Ingresso(**row) if row else None

    def update(self, ingresso: Ingresso):
        cursor = self.db.get_cursor(dictionary=False)
        if not cursor: return False
        query = "UPDATE ingresso SET evento=%s, preco=%s, quantidade_disponivel=%s, data_evento=%s WHERE id=%s"
        cursor.execute(query, (ingresso.evento, ingresso.preco, ingresso.quantidade_disponivel, ingresso.data_evento,
                               ingresso.id))
        self.db.commit()
        cursor.close()
        return True

    def delete(self, id: int):
        cursor = self.db.get_cursor(dictionary=False)
        if not cursor: return False
        cursor.execute("DELETE FROM ingresso WHERE id = %s", (id,))
        self.db.commit()
        cursor.close()
        return True


class CompraRepository(BaseRepository):
    def create(self, compra: CompraIngresso):
        # Restaurada sua transação atômica
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            query_update_estoque = """
                UPDATE ingresso SET quantidade_disponivel = quantidade_disponivel - %s 
                WHERE id = %s AND quantidade_disponivel >= %s
            """
            cursor.execute(query_update_estoque, (compra.quantidade, compra.ingresso_id, compra.quantidade))
            if cursor.rowcount == 0: raise Exception("Estoque insuficiente!")

            query_compra = "INSERT INTO compra_ingresso (usuario_id, ingresso_id, quantidade, valor_total) VALUES (%s, %s, %s, %s)"
            cursor.execute(query_compra, (compra.usuario_id, compra.ingresso_id, compra.quantidade, compra.valor_total))
            conn.commit()
            compra.id = cursor.lastrowid
            return compra
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def find_by_usuario_id(self, usuario_id: int):
        cursor = self.db.get_cursor()
        if not cursor: return []
        query = """
            SELECT c.*, i.evento, i.data_evento FROM compra_ingresso c
            JOIN ingresso i ON c.ingresso_id = i.id
            WHERE c.usuario_id = %s ORDER BY c.data_compra DESC
        """
        cursor.execute(query, (usuario_id,))
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_top_publicos(self):
        cursor = self.db.get_cursor()
        if not cursor: return []
        query = "SELECT i.evento, SUM(c.quantidade) as total_vendido FROM ingresso i JOIN compra_ingresso c ON i.id = c.ingresso_id GROUP BY i.id ORDER BY total_vendido DESC LIMIT 10"
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()
        return res

    def get_top_compradores(self):
        cursor = self.db.get_cursor()
        if not cursor: return []
        query = "SELECT u.nome, COUNT(c.id) as total_compras, SUM(c.valor_total) as total_gasto FROM usuario u JOIN compra_ingresso c ON u.id = c.usuario_id GROUP BY u.id ORDER BY total_gasto DESC LIMIT 10"
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()
        return res
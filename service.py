from repository import UsuarioRepository, IngressoRepository, CompraRepository
from models import Usuario, Ingresso, CompraIngresso
from datetime import datetime
class AuthService:
    def __init__(self):
        self.repo = UsuarioRepository()
        self.usuario_logado = None

    def login(self, email, senha):
        usuario = self.repo.find_by_email(email)
        if usuario and usuario.senha == senha:
            self.usuario_logado = usuario
            return True
        return False

    def logout(self):
        self.usuario_logado = None

class SistemaService:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()
        self.ingresso_repo = IngressoRepository()
        self.compra_repo = CompraRepository()

    # --- USUÁRIOS ---
    def cadastrar_usuario(self, nome, email, senha, tipo='cliente'):
        if self.usuario_repo.find_by_email(email):
            raise Exception("Email já cadastrado!")
        novo_usuario = Usuario(nome=nome, email=email, senha=senha, tipo=tipo)
        return self.usuario_repo.create(novo_usuario)

    def listar_usuarios(self):
        return self.usuario_repo.find_all()

    # --- Ingressos ---
    def cadastrar_ingresso(self, evento, preco, quantidade, data_br):
        try:
            # Tenta ler no formato brasileiro: dd/mm/aaaa hh:mm
            data_obj = datetime.strptime(data_br, "%d/%m/%Y %H:%M")

            # Converte para o formato que o MySQL entende
            data_sql = data_obj.strftime("%Y-%m-%d %H:%M:%S")

        except ValueError:
            raise Exception("Formato de data inválido! Use: DD/MM/YYYY HH:MM")

        if preco < 0 or quantidade < 0:
            raise Exception("Preço ou Quantidade inválidos!")

        novo_ingresso = Ingresso(
            evento=evento,
            preco=preco,
            quantidade_disponivel=quantidade,
            data_evento=data_sql  # Enviamos a data já formatada para o SQL
        )
        return self.ingresso_repo.create(novo_ingresso)

    def listar_ingressos(self):
        return self.ingresso_repo.find_all()

    def buscar_ingresso_por_id(self, id_ingresso):
        return self.ingresso_repo.find_by_id(id_ingresso)

    def atualizar_ingresso(self, id_ingresso, evento=None, preco=None, quantidade=None, data=None):
        ingresso = self.ingresso_repo.find_by_id(id_ingresso)
        if not ingresso: raise Exception("Ingresso não encontrado!")
        
        if evento: ingresso.evento = evento
        if preco is not None: ingresso.preco = preco
        if quantidade is not None: ingresso.quantidade_disponivel = quantidade
        if data: ingresso.data_evento = data
        
        return self.ingresso_repo.update(ingresso)

    def deletar_ingresso(self, id_ingresso):
        if not self.ingresso_repo.find_by_id(id_ingresso):
            raise Exception("Ingresso não encontrado!")
        return self.ingresso_repo.delete(id_ingresso)

    # --- COMPRAS ---
    def realizar_compra(self, usuario_id, ingresso_id, quantidade):
        # Restaurada sua lógica de proteção
        if quantidade <= 0: raise Exception("A quantidade deve ser maior que zero!")
        
        ingresso = self.ingresso_repo.find_by_id(ingresso_id)
        if not ingresso: raise Exception("Ingresso não encontrado!")
        if ingresso.quantidade_disponivel < quantidade:
            raise Exception(f"Quantidade insuficiente! Disponível: {ingresso.quantidade_disponivel}")
        
        valor_total = float(ingresso.preco) * int(quantidade)
        nova_compra = CompraIngresso(usuario_id=usuario_id, ingresso_id=ingresso_id, quantidade=quantidade, valor_total=valor_total)
        return self.compra_repo.create(nova_compra)

    def buscar_compras_por_usuario(self, usuario_id):
        return self.compra_repo.find_by_usuario_id(usuario_id)

    # --- RELATÓRIOS ---
    def obter_maiores_publicos(self):
        return self.compra_repo.get_top_publicos()

    def obter_maiores_compradores(self):
        return self.compra_repo.get_top_compradores()
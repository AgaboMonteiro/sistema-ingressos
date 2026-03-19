from repository import UsuarioRepository, IngressoRepository, CompraRepository
from models import Usuario, Ingresso, CompraIngresso

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

    # --- Usuários ---
    def cadastrar_usuario(self, nome, email, senha, tipo='cliente'):
        if self.usuario_repo.find_by_email(email):
            raise Exception("Email já cadastrado!")
        novo_usuario = Usuario(nome=nome, email=email, senha=senha, tipo=tipo)
        return self.usuario_repo.create(novo_usuario)

    def listar_usuarios(self):
        return self.usuario_repo.find_all()

    # --- Ingressos ---
    def cadastrar_ingresso(self, evento, preco, quantidade, data):
        # Validação simples de formato sem converter o objeto
        if len(data) < 16:  # Ex: "2026-01-01 20:00" tem 16 caracteres
            raise Exception("Formato de data inválido! Use: YYYY-MM-DD HH:MM")

        if preco < 0 or quantidade < 0:
            raise Exception("Preço ou Quantidade inválidos!")

        novo_ingresso = Ingresso(evento=evento, preco=preco, quantidade_disponivel=quantidade, data_evento=data)
        return self.ingresso_repo.create(novo_ingresso)

    def listar_ingressos(self):
        return self.ingresso_repo.find_all()

    # --- Compras ---
    def realizar_compra(self, usuario_id, ingresso_id, quantidade):
        # Validação básica de integridade de entrada
        if quantidade <= 0:
            raise Exception("A quantidade deve ser maior que zero!")

        ingresso = self.ingresso_repo.find_by_id(ingresso_id)
        if not ingresso:
            raise Exception("Ingresso não encontrado!")

        # O Service faz um check prévio para dar feedback rápido ao usuário
        if ingresso.quantidade_disponivel < quantidade:
            raise Exception(f"Quantidade insuficiente! Disponível: {ingresso.quantidade_disponivel}")

        valor_total = float(ingresso.preco) * int(quantidade)
        nova_compra = CompraIngresso(
            usuario_id=usuario_id,
            ingresso_id=ingresso_id,
            quantidade=quantidade,
            valor_total=valor_total
        )
        # O Repository agora é quem garante a integridade final com a transação
        return self.compra_repo.create(nova_compra)

    # --- Relatórios ---
    def obter_maiores_publicos(self):
        return self.compra_repo.get_top_publicos()

    def obter_maiores_compradores(self):
        return self.compra_repo.get_top_compradores()

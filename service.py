# service.py
from repository import UsuarioRepository, IngressoRepository, CompraRepository
from models import Usuario, Ingresso, CompraIngresso
from datetime import datetime
from validators import Validadores  # IMPORTAR O VALIDATORS

# service.py (parte do AuthService)
class AuthService:
    
    def __init__(self):
        self.repo = UsuarioRepository()
        self.usuario_logado = None

    def login(self, email, senha):
        print(f"\n🔍 DEBUG LOGIN:")
        print(f"Email informado: '{email}'")
        print(f"Senha informada: '{senha}'")
        
        # Validar campos vazios no login
        if not email or not email.strip():
            raise Exception("❌ Email não pode ser vazio!")
        if not senha or not senha.strip():
            raise Exception("❌ Senha não pode ser vazia!")
        
        # Buscar usuário no banco
        usuario = self.repo.find_by_email(email.strip())
        
        if usuario:
            print(f"✅ Usuário encontrado no banco:")
            print(f"   ID: {usuario.id}")
            print(f"   Nome: {usuario.nome}")
            print(f"   Email: '{usuario.email}'")
            print(f"   Senha no banco: '{usuario.senha}'")
            print(f"   Tipo: {usuario.tipo}")
            
            # Comparação
            if usuario.senha == senha:
                print("✅ SENHA CORRETA!")
                self.usuario_logado = usuario
                return True
            else:
                print(f"❌ SENHA INCORRETA!")
                print(f"   Senha digitada: '{senha}'")
                print(f"   Senha no banco: '{usuario.senha}'")
                print(f"   São iguais? {usuario.senha == senha}")
        else:
            print(f"❌ Usuário NÃO encontrado com email: '{email}'")
        
        return False

    def logout(self):
        self.usuario_logado = None
class SistemaService:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()
        self.ingresso_repo = IngressoRepository()
        self.compra_repo = CompraRepository()
    
    def _validar_campos_obrigatorios(self, nome, email, senha):
        """Valida os campos usando o Validators"""
        
        # Validar nome
        valido, resultado = Validadores.validar_nome(nome)
        if not valido:
            raise Exception(f"❌ {resultado}")
        nome_validado = resultado
        
        # Validar email
        valido, resultado = Validadores.validar_email(email)
        if not valido:
            raise Exception(f"❌ {resultado}")
        email_validado = resultado
        
        # Validar senha
        valido, resultado = Validadores.validar_senha(senha)
        if not valido:
            raise Exception(f"❌ {resultado}")
        senha_validada = resultado
        
        return nome_validado, email_validado, senha_validada
    
    def buscar_usuario_por_id(self, id_usuario):
        if not id_usuario or id_usuario <= 0:
            raise Exception("❌ ID de usuário inválido!")
        return self.usuario_repo.find_by_id(id_usuario)

    def atualizar_usuario(self, id_usuario, nome=None, email=None, senha=None, tipo=None):
        usuario = self.usuario_repo.find_by_id(id_usuario)
        if not usuario:
            raise Exception("❌ Usuário não encontrado!")
        
        # Validar campos se foram fornecidos
        if nome is not None:
            valido, resultado = Validadores.validar_nome(nome)
            if not valido:
                raise Exception(f"❌ {resultado}")
            usuario.nome = resultado
        
        if email is not None:
            if not email or not email.strip():
                raise Exception("❌ Email não pode ser vazio!")
            
            valido, resultado = Validadores.validar_email(email)
            if not valido:
                raise Exception(f"❌ {resultado}")
            
            # Verificar se email já existe (exceto para o próprio usuário)
            email_existente = self.usuario_repo.find_by_email(resultado)
            if email_existente and email_existente.id != id_usuario:
                raise Exception("❌ Email já cadastrado por outro usuário!")
            usuario.email = resultado
        
        if senha is not None:
            if not senha or not senha.strip():
                raise Exception("❌ Senha não pode ser vazia!")
            
            valido, resultado = Validadores.validar_senha(senha)
            if not valido:
                raise Exception(f"❌ {resultado}")
            usuario.senha = resultado
        
        if tipo is not None:
            if tipo not in ['admin', 'cliente']:
                raise Exception("❌ Tipo inválido! Deve ser 'admin' ou 'cliente'")
            usuario.tipo = tipo
        
        return self.usuario_repo.update(usuario)

    def deletar_usuario(self, id_usuario):
        if not id_usuario or id_usuario <= 0:
            raise Exception("❌ ID de usuário inválido!")
            
        usuario = self.usuario_repo.find_by_id(id_usuario)
        if not usuario:
            raise Exception("❌ Usuário não encontrado!")
        
        # Proteger admin principal (ID 1)
        if id_usuario == 1:
            raise Exception("⚠️ O administrador padrão não pode ser deletado!")
        
        return self.usuario_repo.delete(id_usuario)

    # --- USUÁRIOS ---
    def cadastrar_usuario(self, nome, email, senha, tipo='cliente'):
        # Validar todos os campos usando o Validators
        nome, email, senha = self._validar_campos_obrigatorios(nome, email, senha)
        
        # Validar tipo
        if tipo not in ['admin', 'cliente']:
            raise Exception("❌ Tipo inválido! Deve ser 'admin' ou 'cliente'")
        
        # Verificar se email já existe
        if self.usuario_repo.find_by_email(email):
            raise Exception("❌ Email já cadastrado!")
        
        novo_usuario = Usuario(nome=nome, email=email, senha=senha, tipo=tipo)
        return self.usuario_repo.create(novo_usuario)

    def listar_usuarios(self):
        return self.usuario_repo.find_all()

    # --- Ingressos ---
    def _validar_ingresso(self, evento, preco, quantidade, data_br):
        """Valida campos do ingresso"""
        if not evento or not evento.strip():
            raise Exception("❌ Nome do evento não pode ser vazio!")
        
        if preco <= 0:
            raise Exception("❌ Preço deve ser maior que zero!")
        
        if quantidade <= 0:
            raise Exception("❌ Quantidade deve ser maior que zero!")
        
        if not data_br or not data_br.strip():
            raise Exception("❌ Data do evento não pode ser vazia!")
        
        return evento.strip(), preco, quantidade, data_br.strip()

    def cadastrar_ingresso(self, evento, preco, quantidade, data_br):
        evento, preco, quantidade, data_br = self._validar_ingresso(evento, preco, quantidade, data_br)
        
        try:
            # Tenta ler no formato brasileiro: dd/mm/aaaa hh:mm
            data_obj = datetime.strptime(data_br, "%d/%m/%Y %H:%M")
            # Converte para o formato que o MySQL entende
            data_sql = data_obj.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise Exception("❌ Formato de data inválido! Use: DD/MM/YYYY HH:MM")

        novo_ingresso = Ingresso(
            evento=evento,
            preco=preco,
            quantidade_disponivel=quantidade,
            data_evento=data_sql
        )
        return self.ingresso_repo.create(novo_ingresso)

    def listar_ingressos(self):
        return self.ingresso_repo.find_all()

    def buscar_ingresso_por_id(self, id_ingresso):
        if not id_ingresso or id_ingresso <= 0:
            raise Exception("❌ ID de ingresso inválido!")
        return self.ingresso_repo.find_by_id(id_ingresso)

    def atualizar_ingresso(self, id_ingresso, evento=None, preco=None, quantidade=None, data_br=None):
        ingresso = self.ingresso_repo.find_by_id(id_ingresso)
        if not ingresso: 
            raise Exception("❌ Ingresso não encontrado!")
        
        if evento is not None:
            if not evento or not evento.strip():
                raise Exception("❌ Nome do evento não pode ser vazio!")
            ingresso.evento = evento.strip()
        
        if preco is not None:
            if preco <= 0:
                raise Exception("❌ Preço deve ser maior que zero!")
            ingresso.preco = preco
        
        if quantidade is not None:
            if quantidade <= 0:
                raise Exception("❌ Quantidade deve ser maior que zero!")
            ingresso.quantidade_disponivel = quantidade
        
        if data_br is not None:
            if not data_br or not data_br.strip():
                raise Exception("❌ Data do evento não pode ser vazia!")
            try:
                data_obj = datetime.strptime(data_br.strip(), "%d/%m/%Y %H:%M")
                ingresso.data_evento = data_obj.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise Exception("❌ Formato de data inválido! Use: DD/MM/YYYY HH:MM")
        
        return self.ingresso_repo.update(ingresso)

    def deletar_ingresso(self, id_ingresso):
        if not id_ingresso or id_ingresso <= 0:
            raise Exception("❌ ID de ingresso inválido!")
            
        if not self.ingresso_repo.find_by_id(id_ingresso):
            raise Exception("❌ Ingresso não encontrado!")
        return self.ingresso_repo.delete(id_ingresso)

    # --- COMPRAS ---
    def realizar_compra(self, usuario_id, ingresso_id, quantidade):
        if not usuario_id or usuario_id <= 0:
            raise Exception("❌ Usuário inválido!")
        
        if not ingresso_id or ingresso_id <= 0:
            raise Exception("❌ Ingresso inválido!")
        
        if not quantidade or quantidade <= 0:
            raise Exception("❌ A quantidade deve ser maior que zero!")
        
        ingresso = self.ingresso_repo.find_by_id(ingresso_id)
        if not ingresso:
            raise Exception("❌ Ingresso não encontrado!")
        
        if ingresso.quantidade_disponivel < quantidade:
            raise Exception(f"❌ Quantidade insuficiente! Disponível: {ingresso.quantidade_disponivel}")
        
        valor_total = float(ingresso.preco) * int(quantidade)
        nova_compra = CompraIngresso(
            usuario_id=usuario_id, 
            ingresso_id=ingresso_id, 
            quantidade=quantidade, 
            valor_total=valor_total
        )
        return self.compra_repo.create(nova_compra)

    def buscar_compras_por_usuario(self, usuario_id):
        if not usuario_id or usuario_id <= 0:
            raise Exception("❌ Usuário inválido!")
        return self.compra_repo.find_by_usuario_id(usuario_id)

    # --- RELATÓRIOS ---
    def obter_maiores_publicos(self):
        return self.compra_repo.get_top_publicos()

    def obter_maiores_compradores(self):
        return self.compra_repo.get_top_compradores()
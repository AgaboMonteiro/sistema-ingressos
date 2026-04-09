# service.py
from repository import UsuarioRepository, IngressoRepository, CompraRepository
from models import Usuario, Ingresso, CompraIngresso
from datetime import datetime
from validators import Validadores


class AuthService:
    
    def __init__(self):
        self.repo = UsuarioRepository()
        self.usuario_logado = None

    def login(self, email, senha):
        # Validar campos vazios no login
        if not email or not email.strip():
            raise Exception("❌ Email não pode ser vazio!")
        if not senha or not senha.strip():
            raise Exception("❌ Senha não pode ser vazia!")
        
        # Buscar usuário no banco
        usuario = self.repo.find_by_email(email.strip())
        
        if usuario and usuario.senha == senha:
            self.usuario_logado = usuario
            return True
        
        return False

    def logout(self):
        self.usuario_logado = None


class SistemaService:
    def __init__(self, auth_service=None):
        self.usuario_repo = UsuarioRepository()
        self.ingresso_repo = IngressoRepository()
        self.compra_repo = CompraRepository()
        self.auth_service = auth_service
    
    def _get_usuario_logado(self):
        """Retorna o usuário logado do AuthService"""
        if self.auth_service:
            return self.auth_service.usuario_logado
        return None
    
    def _validar_campos_obrigatorios(self, nome, email, senha):
        """Valida os campos usando o Validators"""
        valido, resultado = Validadores.validar_nome(nome)
        if not valido:
            raise Exception(f"❌ {resultado}")
        nome_validado = resultado
        
        valido, resultado = Validadores.validar_email(email)
        if not valido:
            raise Exception(f"❌ {resultado}")
        email_validado = resultado
        
        valido, resultado = Validadores.validar_senha(senha)
        if not valido:
            raise Exception(f"❌ {resultado}")
        senha_validada = resultado
        
        return nome_validado, email_validado, senha_validada
    
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
    
    # --- USUÁRIOS ---
    def cadastrar_usuario(self, nome, email, senha, tipo='cliente'):
        """Cadastra usuário - qualquer um pode se cadastrar como cliente ou organizador"""
        nome, email, senha = self._validar_campos_obrigatorios(nome, email, senha)
        
        # Permitir cliente ou organizador no cadastro público
        if tipo not in ['organizador', 'cliente']:
            raise Exception("❌ Tipo inválido! Para cadastro público, use 'cliente' ou 'organizador'")
        
        # Verificar se email já existe
        if self.usuario_repo.find_by_email(email):
            raise Exception("❌ Email já cadastrado!")
        
        novo_usuario = Usuario(
            nome=nome, 
            email=email, 
            senha=senha, 
            tipo=tipo
        )
        return self.usuario_repo.create(novo_usuario)
    
    def listar_usuarios(self):
        return self.usuario_repo.find_all()
    
    def buscar_usuario_por_id(self, id_usuario):
        return self.usuario_repo.find_by_id(id_usuario)
    
    def atualizar_usuario(self, id_usuario, nome=None, email=None, senha=None, tipo=None):
        """Atualiza um usuário existente"""
        usuario = self.usuario_repo.find_by_id(id_usuario)
        if not usuario:
            raise Exception("❌ Usuário não encontrado!")
        
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
            if tipo not in ['super_admin', 'organizador', 'cliente']:
                raise Exception("❌ Tipo inválido! Deve ser 'super_admin', 'organizador' ou 'cliente'")
            usuario.tipo = tipo
        
        return self.usuario_repo.update(usuario)
    
    def deletar_usuario(self, id_usuario):
        """Deleta um usuário"""
        if not id_usuario or id_usuario <= 0:
            raise Exception("❌ ID de usuário inválido!")
        
        usuario = self.usuario_repo.find_by_id(id_usuario)
        if not usuario:
            raise Exception("❌ Usuário não encontrado!")
        
        if id_usuario == 1:
            raise Exception("⚠️ O super administrador padrão não pode ser deletado!")
        
        return self.usuario_repo.delete(id_usuario)
    
    # --- INGRESSOS ---
    def cadastrar_ingresso(self, evento, preco, quantidade, data_br):
        """Cadastra ingresso"""
        usuario_logado = self._get_usuario_logado()
        if not usuario_logado or usuario_logado.tipo not in ['super_admin', 'organizador']:
            raise Exception("❌ Apenas administradores e organizadores podem cadastrar eventos!")
        
        evento, preco, quantidade, data_br = self._validar_ingresso(evento, preco, quantidade, data_br)
        
        try:
            data_obj = datetime.strptime(data_br, "%d/%m/%Y %H:%M")
            data_sql = data_obj.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise Exception("❌ Formato de data inválido! Use: DD/MM/YYYY HH:MM")

        novo_ingresso = Ingresso(
            evento=evento,
            preco=preco,
            quantidade_disponivel=quantidade,
            data_evento=data_sql,
            organizador_id=usuario_logado.id
        )
        return self.ingresso_repo.create(novo_ingresso)
    
    def listar_ingressos(self):
        """Lista ingressos conforme permissão do usuário logado"""
        usuario_logado = self._get_usuario_logado()
        if not usuario_logado:
            return self.ingresso_repo.find_all()
        
        if usuario_logado.tipo == 'super_admin':
            return self.ingresso_repo.find_all()
        elif usuario_logado.tipo == 'organizador':
            return self.ingresso_repo.find_by_organizador(usuario_logado.id)
        else:
            return self.ingresso_repo.find_all()
    
    def buscar_ingresso_por_id(self, id_ingresso):
        return self.ingresso_repo.find_by_id(id_ingresso)
    
    def atualizar_ingresso(self, id_ingresso, evento=None, preco=None, quantidade=None, data_br=None):
        """Atualiza ingresso - verifica permissão"""
        usuario_logado = self._get_usuario_logado()
        if not usuario_logado:
            raise Exception("❌ Usuário não logado!")
        
        ingresso = self.ingresso_repo.find_by_id(id_ingresso)
        if not ingresso:
            raise Exception("❌ Ingresso não encontrado!")
        
        # Verificar permissão
        if usuario_logado.tipo == 'super_admin':
            pass
        elif usuario_logado.tipo == 'organizador':
            if ingresso.organizador_id != usuario_logado.id:
                raise Exception("❌ Você só pode alterar seus próprios eventos!")
        else:
            raise Exception("❌ Apenas administradores e organizadores podem alterar eventos!")
        
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
        """Deleta ingresso - verifica permissão"""
        usuario_logado = self._get_usuario_logado()
        if not usuario_logado:
            raise Exception("❌ Usuário não logado!")
        
        ingresso = self.ingresso_repo.find_by_id(id_ingresso)
        if not ingresso:
            raise Exception("❌ Ingresso não encontrado!")
        
        # Verificar permissão
        if usuario_logado.tipo == 'super_admin':
            pass
        elif usuario_logado.tipo == 'organizador':
            if ingresso.organizador_id != usuario_logado.id:
                raise Exception("❌ Você só pode deletar seus próprios eventos!")
        else:
            raise Exception("❌ Apenas administradores e organizadores podem deletar eventos!")
        
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
        return self.compra_repo.find_by_usuario_id(usuario_id)
    
    def buscar_compras_por_ingresso(self, ingresso_id):
        """Busca todas as compras de um ingresso específico"""
        # Por enquanto retorna lista vazia
        return []
    
    # --- RELATÓRIOS ---
    def obter_maiores_publicos(self):
        return self.compra_repo.get_top_publicos()
    
    def obter_maiores_compradores(self):
        return self.compra_repo.get_top_compradores()
    
    def obter_mais_vendidos(self):
        return self.compra_repo.get_mais_vendidos()
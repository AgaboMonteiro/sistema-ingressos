# validators.py
import re

class Validadores:
    
    @staticmethod
    def validar_email(email):
        """Valida formato do email"""
        email = email.strip()
        
        # Padrão de email mais completo
        padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(padrao_email, email):
            return False, "Email deve estar no formato: usuario@dominio.com"
        
        # Verificar domínios comuns
        dominios_validos = ['.com', '.com.br', '.org', '.net', '.edu', '.gov', '.io', '.dev']
        if not any(email.endswith(dominio) for dominio in dominios_validos):
            return False, f"Domínios aceitos: {', '.join(dominios_validos)}"
        
        return True, email
    
    @staticmethod
    def validar_senha(senha):
        """Valida força da senha"""
        senha = senha.strip()
        erros = []
        
        if len(senha) < 8:
            erros.append("mínimo de 8 caracteres")
        
        if not any(c.isupper() for c in senha):
            erros.append("pelo menos uma letra maiúscula")
        
        if not any(c.islower() for c in senha):
            erros.append("pelo menos uma letra minúscula")
        
        if not any(c.isdigit() for c in senha):
            erros.append("pelo menos um número")
        
        if erros:
            return False, f"Senha deve ter: {', '.join(erros)}"
        
        return True, senha
    
    @staticmethod
    def validar_nome(nome):
        """Valida nome"""
        nome = nome.strip()
        
        if not nome:
            return False, "Nome não pode ser vazio"
        
        if len(nome) < 3:
            return False, "Nome deve ter pelo menos 3 caracteres"
        
        return True, nome
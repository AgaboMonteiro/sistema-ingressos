# main.py - CÓDIGO COMPLETO CORRIGIDO
import sys
import os
from datetime import datetime
from service import AuthService, SistemaService

try:
    from tabulate import tabulate
except ImportError:
    def tabulate(data, headers=None, tablefmt=None):
        return str(headers) + "\n" + str(data)


class InterfaceTerminal:
    def __init__(self):
        self.auth_service = AuthService()
        self.sistema_service = SistemaService()
        self.sistema_service.auth_service = self.auth_service

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_titulo(self, texto):
        print("\n" + "=" * 40)
        print(f"{texto.center(40)}")
        print("=" * 40 + "\n")

    def menu_principal(self):
        while True:
            self.limpar_tela()
            self.exibir_titulo("SISTEMA DE INGRESSOS")
            
            print("💡 DICA: Use Ctrl + Scroll do mouse para ZOOM na tela do terminal!\n")

            print("1. Login")
            print("2. Cadastrar como Cliente")
            print("3. Cadastrar como Organizador")
            print("0. Sair")

            opcao = input("\nEscolha uma opção: ")

            if opcao == '1':
                self.tela_login()
            elif opcao == '2':
                self.tela_cadastro_usuario('cliente')
            elif opcao == '3':
                self.tela_cadastro_usuario('organizador')
            elif opcao == '0':
                print("\nSaindo... Até logo!")
                sys.exit()
            else:
                input("\nOpção inválida! Pressione Enter para continuar...")

    def tela_login(self):
        self.limpar_tela()
        self.exibir_titulo("LOGIN")
        email = input("Email: ")
        senha = input("Senha: ")
        try:
            if self.auth_service.login(email, senha):
                self.menu_logado()
            else:
                input("\nCredenciais inválidas! Pressione Enter para tentar novamente...")
        except Exception as e:
            print(f"\nErro: {e}")
            input("\nPressione Enter para voltar...")

    def tela_cadastro_usuario(self, tipo='cliente'):
        """Tela de cadastro de usuário - cliente ou organizador"""
        self.limpar_tela()
        
        tipo_nome = "ORGANIZADOR" if tipo == 'organizador' else "CLIENTE"
        self.exibir_titulo(f"CADASTRO DE {tipo_nome}")
        
        print("📋 REGRAS DE CADASTRO:")
        print("• Nome: mínimo 3 caracteres")
        print("• Email: formato usuario@dominio.com (ex: joao@email.com)")
        print("• Senha: mínimo 8 caracteres, com letras maiúsculas, minúsculas e números")
        print("=" * 40 + "\n")
        
        nome = input("Nome: ").strip()
        email = input("Email: ").strip()
        senha = input("Senha: ").strip()
        
        print(f"\n📌 Você está se cadastrando como {tipo_nome}!")
        if tipo == 'organizador':
            print("   Após o cadastro, você poderá criar e gerenciar seus próprios eventos.")
        else:
            print("   Após o cadastro, você poderá comprar ingressos para os eventos.")
        
        confirmar = input("\nConfirmar cadastro? (s/n): ").lower()
        
        if confirmar != 's':
            print("\nOperação cancelada.")
            input("\nPressione Enter para voltar...")
            return

        try:
            self.sistema_service.cadastrar_usuario(nome, email, senha, tipo=tipo)
            print(f"\n✅ {tipo_nome} cadastrado com sucesso!")
            
        except Exception as e:
            print(f"\n❌ {e}")
        
        input("\nPressione Enter para voltar...")

    def menu_logado(self):
        while self.auth_service.usuario_logado:
            usuario = self.auth_service.usuario_logado
            self.limpar_tela()
            self.exibir_titulo(f"BEM-VINDO, {usuario.nome.upper()}")
            
            print("💡 DICA: Use Ctrl + Scroll do mouse para ZOOM na tela do terminal!\n")
            
            if usuario.tipo == 'super_admin':
                print("👑 SUPER ADMINISTRADOR 👑")
                print("-" * 40)
                print("1. Listar Usuários")
                print("2. Criar Organizador")
                print("3. Atualizar Usuário")
                print("4. Deletar Usuário")
                print("5. Cadastrar Evento")
                print("6. Listar Todos Eventos")
                print("7. Relatório: Mais Vendidos")
                print("0. Logout")
                
                opcao = input("\nEscolha uma opção: ")
                
                if opcao == '0':
                    self.auth_service.logout()
                elif opcao == '1':
                    self.tela_listar_usuarios()
                elif opcao == '2':
                    self.tela_criar_organizador()
                elif opcao == '3':
                    self.tela_atualizar_usuario()
                elif opcao == '4':
                    self.tela_deletar_usuario()
                elif opcao == '5':
                    self.tela_cadastro_ingresso()
                elif opcao == '6':
                    self.tela_listar_ingressos()
                    input("\nPressione Enter para voltar...")
                elif opcao == '7':
                    self.tela_mais_vendidos()
                else:
                    input("\nOpção inválida! Pressione Enter...")
                    
            elif usuario.tipo == 'organizador':
                print("🎫 ORGANIZADOR 🎫")
                print("-" * 40)
                print("1. Cadastrar Evento")
                print("2. Meus Eventos")
                print("0. Logout")
                
                opcao = input("\nEscolha uma opção: ")
                
                if opcao == '0':
                    self.auth_service.logout()
                elif opcao == '1':
                    self.tela_cadastro_ingresso()
                elif opcao == '2':
                    self.tela_listar_ingressos()
                    input("\nPressione Enter para voltar...")
                else:
                    input("\nOpção inválida! Pressione Enter...")
                    
            else:  # cliente
                print("🎟️ CLIENTE 🎟️")
                print("-" * 40)
                print("1. Comprar Ingresso")
                print("2. Listar Eventos Disponíveis")
                print("3. Meus Ingressos Comprados")
                print("4. Eventos Mais Vendidos")
                print("0. Logout")
                
                opcao = input("\nEscolha uma opção: ")
                
                if opcao == '0':
                    self.auth_service.logout()
                elif opcao == '1':
                    self.tela_comprar_ingresso()
                elif opcao == '2':
                    self.tela_listar_ingressos()
                    input("\nPressione Enter para voltar...")
                elif opcao == '3':
                    self.tela_meus_ingressos()
                elif opcao == '4':
                    self.tela_mais_vendidos()
                else:
                    input("\nOpção inválida! Pressione Enter...")

    def tela_cadastro_ingresso(self):
        """Tela para cadastrar um novo ingresso/evento"""
        self.limpar_tela()
        self.exibir_titulo("CADASTRAR EVENTO")
        
        print("📋 DADOS DO EVENTO:\n")
        
        evento = input("Nome do Evento: ").strip()
        
        try:
            preco = float(input("Preço (R$): "))
            quantidade = int(input("Quantidade de ingressos: "))
            
            print("\n📅 DATA DO EVENTO:")
            print("   Exemplo: 25/12/2024")
            
            while True:
                data_str = input("   Data (DD/MM/AAAA): ").strip()
                try:
                    data_obj = datetime.strptime(data_str, "%d/%m/%Y")
                    if data_obj.date() < datetime.now().date():
                        print("   ❌ A data não pode ser no passado! Escolha uma data futura.\n")
                        continue
                    break
                except ValueError:
                    print("   ❌ Data inválida! Use o formato DD/MM/AAAA (ex: 25/12/2024)\n")
            
            print("\n⏰ HORA DO EVENTO:")
            print("   Exemplo: 19:30")
            
            while True:
                hora_str = input("   Hora (HH:MM): ").strip()
                try:
                    datetime.strptime(hora_str, "%H:%M")
                    break
                except ValueError:
                    print("   ❌ Hora inválida! Use o formato HH:MM (ex: 19:30)\n")
            
            data_hora_str = f"{data_str} {hora_str}"
            data_hora_obj = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
            
            if data_hora_obj < datetime.now():
                print("\n⚠️  ATENÇÃO: Esta data e hora já passaram!")
                confirmar = input("Deseja continuar mesmo assim? (s/n): ").lower()
                if confirmar != 's':
                    print("\nOperação cancelada.")
                    input("\nPressione Enter para voltar...")
                    return
            
            print(f"\n📅 Data e hora do evento: {data_hora_str}")
            
            confirmar = input("\nConfirmar cadastro? (s/n): ").lower()
            
            if confirmar == 's':
                self.sistema_service.cadastrar_ingresso(evento, preco, quantidade, data_hora_str)
                print(f"\n✅ Evento cadastrado com sucesso!")
            else:
                print("\nOperação cancelada.")
            
        except ValueError:
            print("\n❌ Erro: Preço e quantidade devem ser números!")
        except Exception as e:
            print(f"\n❌ {e}")
        
        input("\nPressione Enter para voltar...")

    def tela_listar_ingressos(self):
        self.limpar_tela()
        self.exibir_titulo("EVENTOS DISPONÍVEIS")
        
        ingressos = self.sistema_service.listar_ingressos()
        if ingressos:
            data = [[i.id, i.evento, f"R${i.preco:.2f}", i.quantidade_disponivel, i.data_evento] for i in ingressos]
            print(tabulate(data, headers=["ID", "Evento", "Preço", "Quantidade", "Data"], tablefmt="grid"))
        else:
            print("Nenhum evento disponível.")
        
        print("\n0. Voltar")
        return ingressos

    def tela_comprar_ingresso(self):
        ingressos = self.tela_listar_ingressos()
        if not ingressos:
            input("\nPressione Enter para voltar...")
            return
        try:
            id_ingresso = int(input("\nID do Ingresso: "))
            quantidade = int(input("Quantidade: "))
            self.sistema_service.realizar_compra(self.auth_service.usuario_logado.id, id_ingresso, quantidade)
            print("\n✅ Compra realizada com sucesso!")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        input("\nPressione Enter para voltar...")

    def tela_meus_ingressos(self):
        self.limpar_tela()
        self.exibir_titulo("MEUS INGRESSOS")
        
        compras = self.sistema_service.buscar_compras_por_usuario(self.auth_service.usuario_logado.id)
        if compras:
            data = [[c['id'], c['evento'], c['quantidade'], f"R${c['valor_total']:.2f}"] for c in compras]
            print(tabulate(data, headers=["ID", "Evento", "Quantidade", "Total"], tablefmt="grid"))
        else:
            print("Nenhuma compra realizada.")
        
        print("\n0. Voltar")
        input("\nPressione Enter para voltar...")

    def tela_mais_vendidos(self):
        """Mostra os eventos mais vendidos"""
        self.limpar_tela()
        self.exibir_titulo("🎯 EVENTOS MAIS VENDIDOS")
        
        try:
            resultados = self.sistema_service.obter_mais_vendidos()
            
            if resultados:
                data = []
                for item in resultados:
                    data.append([
                        item['id'],
                        item['evento'],
                        f"R$ {float(item['preco']):.2f}",
                        item['data_evento'],
                        item['total_vendido']
                    ])
                
                print(tabulate(
                    data,
                    headers=["ID", "Evento", "Preço", "Data", "Quantidade Vendida"],
                    tablefmt="grid"
                ))
            else:
                print("Nenhum evento encontrado ou ainda não há vendas.")
                
        except Exception as e:
            print(f"Erro: {e}")
        
        print("\n0. Voltar")
        input("\nPressione Enter para voltar...")

    def tela_listar_usuarios(self):
        """Lista todos os usuários (super_admin apenas)"""
        self.limpar_tela()
        self.exibir_titulo("LISTA DE USUÁRIOS")
        
        try:
            usuarios = self.sistema_service.listar_usuarios()
            if usuarios:
                data = [[u.id, u.nome, u.email, u.tipo] for u in usuarios]
                print(tabulate(data, headers=["ID", "Nome", "Email", "Tipo"], tablefmt="grid"))
            else:
                print("Nenhum usuário encontrado.")
        except Exception as e:
            print(f"Erro: {e}")
        
        print("\n0. Voltar")
        input("\nPressione Enter para voltar...")

    def tela_criar_organizador(self):
        """Cria um novo organizador (super_admin apenas)"""
        self.limpar_tela()
        self.exibir_titulo("CRIAR ORGANIZADOR")
        
        nome = input("Nome: ").strip()
        email = input("Email: ").strip()
        senha = input("Senha: ").strip()
        
        try:
            self.sistema_service.cadastrar_usuario(nome, email, senha, tipo='organizador')
            print("\n✅ Organizador criado com sucesso!")
        except Exception as e:
            print(f"\n❌ {e}")
        
        print("\n0. Voltar")
        input("\nPressione Enter para voltar...")

    def tela_atualizar_usuario(self):
        """Atualiza dados de um usuário (super_admin apenas)"""
        self.limpar_tela()
        self.exibir_titulo("ATUALIZAR USUÁRIO")
        
        usuarios = self.sistema_service.listar_usuarios()
        if not usuarios:
            print("Nenhum usuário encontrado.")
            input("\n0. Voltar")
            return
        
        data = [[u.id, u.nome, u.email, u.tipo] for u in usuarios]
        print(tabulate(data, headers=["ID", "Nome", "Email", "Tipo"], tablefmt="grid"))
        
        try:
            id_usuario = int(input("\nID do usuário para atualizar: "))
            
            if id_usuario == 1:
                print("\n⚠️ Administrador padrão não pode ser alterado!")
                input("\n0. Voltar")
                return
            
            print("\nDeixe em branco para manter o valor atual")
            novo_nome = input("Novo nome: ").strip() or None
            novo_email = input("Novo email: ").strip() or None
            nova_senha = input("Nova senha: ").strip() or None
            
            self.sistema_service.atualizar_usuario(id_usuario, novo_nome, novo_email, nova_senha)
            print("\n✅ Usuário atualizado com sucesso!")
            
        except Exception as e:
            print(f"\n❌ {e}")
        
        print("\n0. Voltar")
        input("\nPressione Enter para voltar...")

    def tela_deletar_usuario(self):
        """Deleta um usuário (super_admin apenas)"""
        self.limpar_tela()
        self.exibir_titulo("DELETAR USUÁRIO")
        
        usuarios = self.sistema_service.listar_usuarios()
        if not usuarios:
            print("Nenhum usuário encontrado.")
            input("\n0. Voltar")
            return
        
        data = [[u.id, u.nome, u.email, u.tipo] for u in usuarios]
        print(tabulate(data, headers=["ID", "Nome", "Email", "Tipo"], tablefmt="grid"))
        
        try:
            id_usuario = int(input("\nID do usuário para deletar: "))
            
            if id_usuario == 1:
                print("\n⚠️ Administrador padrão não pode ser deletado!")
                input("\n0. Voltar")
                return
            
            if id_usuario == self.auth_service.usuario_logado.id:
                print("\n❌ Você não pode deletar seu próprio usuário!")
                input("\n0. Voltar")
                return
            
            confirmar = input(f"\nTem certeza que deseja deletar o usuário ID {id_usuario}? (s/n): ")
            if confirmar.lower() == 's':
                self.sistema_service.deletar_usuario(id_usuario)
                print("\n✅ Usuário deletado com sucesso!")
            else:
                print("\nOperação cancelada.")
            
        except Exception as e:
            print(f"\n❌ {e}")
        
        print("\n0. Voltar")
        input("\nPressione Enter para voltar...")


if __name__ == "__main__":
    app = InterfaceTerminal()
    app.menu_principal()
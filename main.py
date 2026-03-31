# main.py
import sys
import os
from service import AuthService, SistemaService

# Importar tabulate de forma segura
try:
    from tabulate import tabulate
except ImportError:
    def tabulate(data, headers=None, tablefmt=None):
        return str(headers) + "\n" + str(data)


class InterfaceTerminal:
    def __init__(self):
        self.auth_service = AuthService()
        self.sistema_service = SistemaService()

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

            print("1. Login")
            print("2. Cadastrar Novo Usuário")
            print("0. Sair")

            opcao = input("\nEscolha uma opção: ")

            if opcao == '1':
                self.tela_login()
            elif opcao == '2':
                self.tela_cadastro_usuario()
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
            print("\n" + "!" * 40)
            print("ERRO DE CONEXÃO COM O BANCO AIVEN")
            print("!" * 40)
            print(f"Detalhe do Erro: {e}")
            print("\nVerifique se:")
            print("1. Sua senha está correta no arquivo 'config.py'.")
            print("2. Seu IP está liberado no painel do Aiven.")
            print("3. Você tem conexão com a internet.")
            input("\nPressione Enter para voltar...")

    def tela_cadastro_usuario(self):  # ← LINHA 71
        """Tela de cadastro de usuário"""
        self.limpar_tela()  # ← ESTA LINHA DEVE ESTAR INDENTADA
        self.exibir_titulo("CADASTRO DE USUÁRIO")
        
        print("📋 REGRAS DE CADASTRO:")
        print("• Nome: mínimo 3 caracteres")
        print("• Email: formato usuario@dominio.com (ex: joao@email.com)")
        print("• Senha: mínimo 8 caracteres, com letras maiúsculas, minúsculas e números")
        print("=" * 40 + "\n")
        
        nome = input("Nome: ").strip()
        email = input("Email: ").strip()
        senha = input("Senha: ").strip()

        try:
            self.sistema_service.cadastrar_usuario(nome, email, senha)
            print("\n✅ Usuário cadastrado com sucesso!")
            print("\n🔐 Dicas de segurança:")
            print("• Nunca compartilhe sua senha")
            print("• Use uma senha diferente para cada serviço")
            
        except Exception as e:
            print(f"\n❌ {e}")
            print("\n📌 Exemplos válidos:")
            print("   Email: joaosilva@email.com")
            print("   Senha: MinhaSenha123")
        
        input("\nPressione Enter para voltar...")

    def menu_logado(self):
        while self.auth_service.usuario_logado:
            usuario = self.auth_service.usuario_logado

            self.limpar_tela()
            self.exibir_titulo(f"BEM-VINDO, {usuario.nome.upper()}")

            if usuario.tipo == 'admin':
                self.menu_admin()
            else:
                self.menu_cliente()

    def menu_admin(self):
        """Menu do administrador com todas as opções"""
        print("1. Cadastrar Ingresso")
        print("2. Listar Ingressos")
        print("3. Atualizar Ingresso")
        print("4. Deletar Ingresso")
        print("5. Listar Usuários")
        print("6. Atualizar Usuário")
        print("7. Deletar Usuário")
        print("8. Relatório: Maiores Públicos (Top 10)")
        print("9. Relatório: Maiores Compradores (Top 10)")
        print("0. Logout")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            self.tela_cadastro_ingresso()
        elif opcao == '2':
            self.tela_listar_ingressos()
            input("\nPressione Enter para continuar...")
        elif opcao == '3':
            self.tela_atualizar_ingresso()
        elif opcao == '4':
            self.tela_deletar_ingresso()
        elif opcao == '5':
            self.tela_listar_usuarios()
        elif opcao == '6':
            self.tela_atualizar_usuario()
        elif opcao == '7':
            self.tela_deletar_usuario()
        elif opcao == '8':
            self.tela_relatorio_publicos()
        elif opcao == '9':
            self.tela_relatorio_compradores()
        elif opcao == '0':
            self.auth_service.logout()
        else:
            input("\nOpção inválida! Pressione Enter...")

    def menu_cliente(self):
        """Menu do cliente com novas opções"""
        print("1. Comprar Ingresso")
        print("2. Listar Eventos Disponíveis")
        print("3. Meus Ingressos Comprados")
        print("0. Logout")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            self.tela_comprar_ingresso()
        elif opcao == '2':
            self.tela_listar_ingressos()
            input("\nPressione Enter para voltar...")
        elif opcao == '3':
            self.tela_meus_ingressos()
        elif opcao == '0':
            self.auth_service.logout()
        else:
            input("\nOpção inválida! Pressione Enter...")

    def tela_cadastro_ingresso(self):
        self.limpar_tela()
        self.exibir_titulo("CADASTRAR EVENTO")

        evento = input("Nome do Evento: ")

        try:
            preco = float(input("Preço: "))
            quantidade = int(input("Quantidade: "))
            data = input("Data (DD/MM/YYYY HH:MM): ")

            self.sistema_service.cadastrar_ingresso(evento, preco, quantidade, data)

            input("\nEvento cadastrado! Pressione Enter...")

        except ValueError:
            input("\nErro: Preço ou Quantidade devem ser números! Pressione Enter...")

        except Exception as e:
            input(f"\nErro: {e}")

    def tela_listar_usuarios(self):
        self.limpar_tela()

        try:
            usuarios = self.sistema_service.listar_usuarios()

            if usuarios:
                data = [[u.id, u.nome, u.email, u.tipo] for u in usuarios]
                print(tabulate(
                    data,
                    headers=["ID", "Nome", "Email", "Tipo"],
                    tablefmt="grid"
                ))
            else:
                print("Nenhum usuário encontrado.")

        except Exception as e:
            print(f"Erro ao listar usuários: {e}")

        input("\nPressione Enter para voltar...")

    def tela_relatorio_publicos(self):
        self.limpar_tela()
        self.exibir_titulo("TOP 10 MAIORES PÚBLICOS")

        try:
            dados = self.sistema_service.obter_maiores_publicos()

            if dados:
                if isinstance(dados[0], dict):
                    print(tabulate(dados, headers="keys", tablefmt="grid"))
                else:
                    print(tabulate(
                        dados,
                        headers=["Evento", "Total Vendido"],
                        tablefmt="grid"
                    ))
            else:
                print("Nenhum dado disponível.")

        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")

        input("\nPressione Enter para voltar...")

    def tela_relatorio_compradores(self):
        self.limpar_tela()
        self.exibir_titulo("TOP 10 MAIORES COMPRADORES")

        try:
            dados = self.sistema_service.obter_maiores_compradores()

            if dados:
                if isinstance(dados[0], dict):
                    print(tabulate(dados, headers="keys", tablefmt="grid"))
                else:
                    print(tabulate(
                        dados,
                        headers=["Nome", "Total Compras", "Total Gasto (R$)"],
                        tablefmt="grid"
                    ))
            else:
                print("Nenhum dado disponível.")

        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")

        input("\nPressione Enter para voltar...")

    def tela_listar_ingressos(self):
        self.limpar_tela()
        self.exibir_titulo("EVENTOS DISPONÍVEIS")

        try:
            ingressos = self.sistema_service.listar_ingressos()

            if ingressos:
                data = [
                    [i.id, i.evento, f"R$ {float(i.preco):.2f}", i.quantidade_disponivel, i.data_evento]
                    for i in ingressos
                ]

                print(tabulate(
                    data,
                    headers=["ID", "Evento", "Preço", "Qtd", "Data"],
                    tablefmt="grid"
                ))

                return ingressos
            else:
                print("Nenhum evento disponível.")

        except Exception as e:
            print(f"Erro ao listar eventos: {e}")

        return []

    def tela_comprar_ingresso(self):
        ingressos = self.tela_listar_ingressos()

        if not ingressos:
            input("\nPressione Enter para voltar...")
            return

        try:
            id_ingresso = int(input("\nID do Ingresso: "))
            quantidade = int(input("Quantidade: "))

            self.sistema_service.realizar_compra(
                self.auth_service.usuario_logado.id,
                id_ingresso,
                quantidade
            )

            input("\nCompra realizada com sucesso! Pressione Enter...")

        except ValueError:
            input("\nErro: Digite números válidos para ID e Quantidade! Pressione Enter...")

        except Exception as e:
            input(f"\nErro: {e}\nPressione Enter...")

    def tela_atualizar_ingresso(self):
        """Tela para atualizar um ingresso"""
        self.limpar_tela()
        self.exibir_titulo("ATUALIZAR INGRESSO")

        ingressos = self.sistema_service.listar_ingressos()
        if not ingressos:
            print("Nenhum ingresso cadastrado.")
            input("\nPressione Enter para voltar...")
            return

        data_tabela = []
        for i in ingressos:
            data_formatada = i.data_evento.strftime("%d/%m/%Y %H:%M") if hasattr(i.data_evento, 'strftime') else i.data_evento
            data_tabela.append([i.id, i.evento, f"R${i.preco:.2f}", i.quantidade_disponivel, data_formatada])

        print(tabulate(data_tabela, headers=["ID", "Evento", "Preço", "Qtd", "Data"], tablefmt="grid"))

        try:
            id_ingresso = int(input("\nID do ingresso que deseja atualizar: "))
            ingresso = self.sistema_service.buscar_ingresso_por_id(id_ingresso)

            if not ingresso:
                print("Ingresso não encontrado!")
                input("\nPressione Enter para voltar...")
                return

            data_atual_br = ingresso.data_evento.strftime("%d/%m/%Y %H:%M") if hasattr(ingresso.data_evento, 'strftime') else ingresso.data_evento

            print(f"\nAtualizando: {ingresso.evento}")
            print("(Deixe em branco para manter o valor atual)")

            novo_evento = input(f"Novo nome do evento [{ingresso.evento}]: ").strip()

            try:
                novo_preco_str = input(f"Novo preço [R${ingresso.preco:.2f}]: ").strip()
                novo_preco = float(novo_preco_str) if novo_preco_str else None
            except ValueError:
                print("Preço inválido! Mantendo valor atual.")
                novo_preco = None

            try:
                nova_qtd_str = input(f"Nova quantidade [{ingresso.quantidade_disponivel}]: ").strip()
                nova_qtd = int(nova_qtd_str) if nova_qtd_str else None
            except ValueError:
                print("Quantidade inválida! Mantendo valor atual.")
                nova_qtd = None

            nova_data_br = input(f"Nova data [{data_atual_br}]: ").strip()

            print("\n" + "=" * 40)
            print("RESUMO DA ATUALIZAÇÃO:")
            if novo_evento: print(f"Evento: {ingresso.evento} -> {novo_evento}")
            if novo_preco: print(f"Preço: R${ingresso.preco:.2f} -> R${novo_preco:.2f}")
            if nova_qtd: print(f"Quantidade: {ingresso.quantidade_disponivel} -> {nova_qtd}")
            if nova_data_br: print(f"Data: {data_atual_br} -> {nova_data_br}")

            confirmar = input("\nConfirmar atualização? (s/n): ").lower()

            if confirmar == 's':
                self.sistema_service.atualizar_ingresso(
                    id_ingresso,
                    evento=novo_evento if novo_evento else None,
                    preco=novo_preco,
                    quantidade=nova_qtd,
                    data_br=nova_data_br if nova_data_br else None
                )
                print("\n✅ Ingresso atualizado com sucesso!")
            else:
                print("\nOperação cancelada.")

        except ValueError:
            print("\nErro: ID inválido!")
        except Exception as e:
            print(f"\nErro: {e}")

        input("\nPressione Enter para voltar...")

    def tela_deletar_ingresso(self):
        """Tela para deletar um ingresso"""
        self.limpar_tela()
        self.exibir_titulo("DELETAR INGRESSO")
        
        ingressos = self.sistema_service.listar_ingressos()
        if not ingressos:
            print("Nenhum ingresso cadastrado.")
            input("\nPressione Enter para voltar...")
            return
        
        data = [[i.id, i.evento, f"R${i.preco:.2f}", i.quantidade_disponivel, i.data_evento] 
                for i in ingressos]
        print(tabulate(data, headers=["ID", "Evento", "Preço", "Qtd", "Data"], tablefmt="grid"))
        
        try:
            id_ingresso = int(input("\nID do ingresso que deseja deletar: "))
            ingresso = self.sistema_service.buscar_ingresso_por_id(id_ingresso)
            
            if not ingresso:
                print("Ingresso não encontrado!")
                input("\nPressione Enter para voltar...")
                return
            
            print(f"\nVocê está prestes a deletar:")
            print(f"Evento: {ingresso.evento}")
            print(f"Preço: R${ingresso.preco:.2f}")
            print(f"Quantidade: {ingresso.quantidade_disponivel}")
            print(f"Data: {ingresso.data_evento}")
            
            print("\n⚠️  ATENÇÃO: Esta ação não pode ser desfeita!")
            
            confirmar = input("\nDigite 'DELETAR' para confirmar: ").strip().upper()
            
            if confirmar == 'DELETAR':
                self.sistema_service.deletar_ingresso(id_ingresso)
                print("\n✅ Ingresso deletado com sucesso!")
            else:
                print("\nOperação cancelada.")
            
        except ValueError:
            print("\nErro: ID inválido!")
        except Exception as e:
            print(f"\nErro: {e}")
        
        input("\nPressione Enter para voltar...")

    def tela_atualizar_usuario(self):
        """Tela para atualizar um usuário"""
        self.limpar_tela()
        self.exibir_titulo("ATUALIZAR USUÁRIO")
        
        usuarios = self.sistema_service.listar_usuarios()
        if not usuarios:
            print("Nenhum usuário cadastrado.")
            input("\nPressione Enter para voltar...")
            return
        
        data = [[u.id, u.nome, u.email, u.tipo] for u in usuarios]
        print(tabulate(data, headers=["ID", "Nome", "Email", "Tipo"], tablefmt="grid"))
        
        try:
            id_usuario = int(input("\nID do usuário que deseja atualizar: "))
            
            if id_usuario == 1:
                print("\n⚠️  O administrador padrão não pode ser alterado por segurança!")
                input("\nPressione Enter para voltar...")
                return
            
            usuario = self.sistema_service.buscar_usuario_por_id(id_usuario)
            
            if not usuario:
                print("Usuário não encontrado!")
                input("\nPressione Enter para voltar...")
                return
            
            print(f"\nAtualizando: {usuario.nome}")
            print("(Deixe em branco para manter o valor atual)")
            print("\n📋 REGRAS DE VALIDAÇÃO:")
            print("• Nome: mínimo 3 caracteres")
            print("• Email: formato usuario@dominio.com")
            print("• Senha: mínimo 8 caracteres, com maiúsculas, minúsculas e números\n")
            
            novo_nome = input(f"Novo nome [{usuario.nome}]: ").strip()
            if novo_nome == "":
                novo_nome = None
            
            novo_email = input(f"Novo email [{usuario.email}]: ").strip()
            if novo_email == "":
                novo_email = None
            
            nova_senha = input("Nova senha (deixe em branco para não alterar): ").strip()
            if nova_senha == "":
                nova_senha = None
            
            print("\nTipos disponíveis: admin, cliente")
            tipo_atual = usuario.tipo
            novo_tipo_input = input(f"Novo tipo [{tipo_atual}]: ").strip()
            novo_tipo = novo_tipo_input if novo_tipo_input in ['admin', 'cliente'] else None
            
            print("\n" + "=" * 40)
            print("RESUMO DA ATUALIZAÇÃO:")
            if novo_nome: print(f"Nome: {usuario.nome} -> {novo_nome}")
            if novo_email: print(f"Email: {usuario.email} -> {novo_email}")
            if nova_senha: print("Senha: [alterada]")
            if novo_tipo: print(f"Tipo: {usuario.tipo} -> {novo_tipo}")
            
            confirmar = input("\nConfirmar atualização? (s/n): ").lower()
            
            if confirmar == 's':
                self.sistema_service.atualizar_usuario(
                    id_usuario,
                    nome=novo_nome,
                    email=novo_email,
                    senha=nova_senha,
                    tipo=novo_tipo
                )
                print("\n✅ Usuário atualizado com sucesso!")
            else:
                print("\nOperação cancelada.")
            
        except ValueError:
            print("\nErro: ID inválido!")
        except Exception as e:
            print(f"\nErro: {e}")
        
        input("\nPressione Enter para voltar...")

    def tela_deletar_usuario(self):
        """Tela para deletar um usuário"""
        self.limpar_tela()
        self.exibir_titulo("DELETAR USUÁRIO")
        
        usuarios = self.sistema_service.listar_usuarios()
        if not usuarios:
            print("Nenhum usuário cadastrado.")
            input("\nPressione Enter para voltar...")
            return
        
        data = [[u.id, u.nome, u.email, u.tipo] for u in usuarios]
        print(tabulate(data, headers=["ID", "Nome", "Email", "Tipo"], tablefmt="grid"))
        
        try:
            id_usuario = int(input("\nID do usuário que deseja deletar: "))
            
            if id_usuario == self.auth_service.usuario_logado.id:
                print("\n❌ Erro: Você não pode deletar seu próprio usuário!")
                input("\nPressione Enter para voltar...")
                return
            
            if id_usuario == 1:
                print("\n⚠️  O administrador padrão não pode ser deletado!")
                input("\nPressione Enter para voltar...")
                return
            
            usuario = self.sistema_service.buscar_usuario_por_id(id_usuario)
            
            if not usuario:
                print("Usuário não encontrado!")
                input("\nPressione Enter para voltar...")
                return
            
            print(f"\nVocê está prestes a deletar:")
            print(f"Nome: {usuario.nome}")
            print(f"Email: {usuario.email}")
            print(f"Tipo: {usuario.tipo}")
            
            print("\n⚠️  ATENÇÃO: Todas as compras deste usuário também serão deletadas!")
            
            confirmar = input("\nDigite 'DELETAR' para confirmar: ").strip().upper()
            
            if confirmar == 'DELETAR':
                self.sistema_service.deletar_usuario(id_usuario)
                print("\n✅ Usuário deletado com sucesso!")
            else:
                print("\nOperação cancelada.")
            
        except ValueError:
            print("\nErro: ID inválido!")
        except Exception as e:
            print(f"\nErro: {e}")
        
        input("\nPressione Enter para voltar...")
    
    def tela_meus_ingressos(self):
        """Mostra os ingressos comprados pelo cliente"""
        self.limpar_tela()
        self.exibir_titulo("MEUS INGRESSOS COMPRADOS")
        
        try:
            usuario_id = self.auth_service.usuario_logado.id
            compras = self.sistema_service.buscar_compras_por_usuario(usuario_id)
            
            if not compras:
                print("📭 Você ainda não comprou nenhum ingresso.")
                print("\nQue tal conferir os eventos disponíveis? (opção 2)")
            else:
                data = []
                total_gasto = 0
                
                for compra in compras:
                    data_compra = compra['data_compra'].strftime("%d/%m/%Y %H:%M") if hasattr(compra['data_compra'], 'strftime') else compra['data_compra']
                    data_evento = compra['data_evento'].strftime("%d/%m/%Y %H:%M") if hasattr(compra['data_evento'], 'strftime') else compra['data_evento']
                    
                    valor_compra = float(compra['valor_total'])
                    total_gasto += valor_compra
                    
                    data.append([
                        compra['id'],
                        compra['evento'],
                        data_evento,
                        compra['quantidade'],
                        f"R${valor_compra:.2f}",
                        data_compra
                    ])
                
                print(tabulate(
                    data,
                    headers=["ID Compra", "Evento", "Data do Evento", "Qtd", "Total Pago", "Data da Compra"],
                    tablefmt="grid"
                ))
                
                total_compras = len(compras)
                total_ingressos = sum(c['quantidade'] for c in compras)
                
                print("\n" + "=" * 40)
                print("📊 RESUMO:")
                print(f"Total de compras realizadas: {total_compras}")
                print(f"Total de ingressos adquiridos: {total_ingressos}")
                print(f"Total gasto: R${total_gasto:.2f}")
                print("=" * 40)
                
        except Exception as e:
            print(f"\nErro ao buscar seus ingressos: {e}")
            import traceback
            traceback.print_exc()
        
        input("\nPressione Enter para voltar...")


if __name__ == "__main__":
    app = InterfaceTerminal()
    app.menu_principal()
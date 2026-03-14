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

    def tela_cadastro_usuario(self):
        self.limpar_tela()
        self.exibir_titulo("CADASTRO DE USUÁRIO")

        nome = input("Nome: ")
        email = input("Email: ")
        senha = input("Senha: ")

        try:
            self.sistema_service.cadastrar_usuario(nome, email, senha)
            input("\nUsuário cadastrado com sucesso! Pressione Enter para voltar...")
        except Exception as e:
            input(f"\nErro: {e}\nPressione Enter para voltar...")

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

        print("1. Cadastrar Ingresso")
        print("2. Listar Usuários")
        print("3. Relatório: Maiores Públicos (Top 10)")
        print("4. Relatório: Maiores Compradores (Top 10)")
        print("0. Logout")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            self.tela_cadastro_ingresso()

        elif opcao == '2':
            self.tela_listar_usuarios()

        elif opcao == '3':
            self.tela_relatorio_publicos()

        elif opcao == '4':
            self.tela_relatorio_compradores()

        elif opcao == '0':
            self.auth_service.logout()

        else:
            input("\nOpção inválida!")

    def menu_cliente(self):

        print("1. Comprar Ingresso")
        print("2. Listar Eventos Disponíveis")
        print("0. Logout")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            self.tela_comprar_ingresso()

        elif opcao == '2':
            self.tela_listar_ingressos()
            input("\nPressione Enter para voltar...")

        elif opcao == '0':
            self.auth_service.logout()

        else:
            input("\nOpção inválida!")

    def tela_cadastro_ingresso(self):

        self.limpar_tela()
        self.exibir_titulo("CADASTRAR EVENTO")

        evento = input("Nome do Evento: ")

        try:
            preco = float(input("Preço: "))
            quantidade = int(input("Quantidade: "))
            data = input("Data (YYYY-MM-DD HH:MM): ")

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


if __name__ == "__main__":

    app = InterfaceTerminal()
    app.menu_principal()
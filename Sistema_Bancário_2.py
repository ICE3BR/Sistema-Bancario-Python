import datetime
import textwrap
date = datetime.datetime.now()
data = date.strftime("%d-%m-%Y|%H:%M")

def menu():
    menu = """\n
[1]\tSaque
[2]\tDepósito 
[3]\tExtrato 
[4]\tNova Usuário
[5]\tNovo Conta
[6]\tListar Contas
[0]\tSair
=>> """
    return input(textwrap.dedent(menu))

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    
    if excedeu_saldo: # Mensagem avisando: Saldo insuficiente
        print("\n@@@ Operação falhou! | Você não tem saldo suficiente. @@@")
        print(f"SALDO: R$ {saldo:.2f} | Valor Pedido de Saque: R$ {valor:.2f}")

    elif excedeu_limite: # Mensagem avisando: Valor excede o limite disponível por saque
        print("\n@@@ Operação falhou! | O valor do saque excede o limite. @@@")
        print(f"Limite disponível por saque: R$ {limite:.2f}")
        print(f"Valor Pedido: R$ {valor:.2f}")

    elif excedeu_saques: # Mensagem avisando: Atingiu o limite de saques
        print("\n@@@ Operação falhou! | Número máximo de saques excedido. @@@")
        print(f"Os Limites de Saques mensais foram atingidos: {numero_saques}")

    elif valor > 0: # Condição true para saque
        saldo -= valor
        extrato += f"{data}|\tSaque:\t\tR$ -{valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! | Valor inválido! @@@")

    return saldo, extrato

def depositar(saldo, valor, extrato, /):
    if (valor > 0): # Condição True para deposito #
        saldo += valor
        extrato += f"{data}|\tDeposito:\t\tR$ +{valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else: # Condição False para deposito
        print("\n@@@ Operação falhou! | Valor inválido! @@@")
        print("--"*20)
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações.\n" if not extrato else f"Extrato Bancário:\n{extrato}")
    print(f"Saldo Atual:\tR$ {saldo:.2f}")
    print("="*41)

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, numero - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, criação da conta encerrada! @@@")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "2":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "1":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "0":
            break

        else:
            print("Operação Inválida, Tente Novamente")
            print("--"*20)
            continue


main()
import datetime

saldo = 0
limite = 500
extrato = ""
numero_saque = 0
LIMITE_SAQUE = 3
date = datetime.datetime.now()
data = date.strftime("%d-%m-%Y|%H:%M")

while True:
    opcao = int(input("[1] Saque:\n[2] Depósito \n[3] Extrato \n[0] Sair \n: "))
    
    if opcao == 1:
        saque = float(input("Sacar: R$ "))
        print("--"*20)
        if (saldo >= saque and saque > 0 and saque <= limite and numero_saque < LIMITE_SAQUE): # Condição True para saque #
            saldo -= saque
            numero_saque += 1
            extrato += f"{data}: Saque: R$ -{saque:.2f}\n"
        
            print(f"""
Permissão Saque: Aceita
Você Sacou: R$ {saque:.2f}
Saldo Atual da conta: R$ {saldo:.2f}
            """)
        
        else: # Condição False para saque #
            if (saque <= 0): # Mensagem avisando: o valor não pode ser negativo ou 0
                print(f"O valor não pode ser negativo ou 0\nTente novante")
            elif (saque > limite): # Mensagem avisando: o valor passou do limite disponível por saque
                print(f"Permissão Saque: Negada | Limite Insuficiente")
                print(f"Valor pedido de saque: R$ {saque:.2f}")
                print(f"Valor pedido está acima do Limite disponível por saque: R$ {limite:.2f}")
            elif (saldo < saque): # Mensagem avisando: Falta Saldo na conta
                print(f"Permissão Saque: Negada | Saldo Insuficiente")
                print(f"SALDO: R$ {saldo:.2f} | Valor Pedido de Saque: R$ {saque:.2f}")
            elif (numero_saque == LIMITE_SAQUE): # Mensagem avisando: Atingiu o limite de saques
                print(f"Permissão Saque: Negada | Limite de Saques Atingidos")
                print(f"Os Limites de Saques mensais foram atingidos: {numero_saque}")
            else: # Mensagem avisando: Falta Saldo e Limite para realizar o saque
                print(f"Permissão Saque: Negada | Saldo e Limites Insuficientes")
                print(f"SALDO: R$ {saldo:.2f} | Valor Pedido de Saque: R$ {saque:.2f}")
                print(f"Os Limites de Saques mensais foram atingidos: {numero_saque}")
                print(f"Valor acima do Limite por Saque: R$ {limite:.2f}")
        print("--"*20)

    elif opcao == 2:    
        deposito = float(input("Depositar: R$ "))
        print("--"*20)
        if (deposito > 0): # Condição True para deposito #
            saldo += deposito
            extrato += f"{data}: Deposito: R$ +{deposito:.2f}\n"

            print(f"""
Permissão Depósito: Aceita
Você Depositou: R$ {deposito:.2f}
Saldo Atual da conta: R$ {saldo:.2f}
            """)

        else: # Condição False para deposito #
            print(f"Valor a ser depositado é Negativo.\nPor favor coloque um valor válido")
            print("--"*20)

    elif opcao == 3:
        print("Não foram realizadas movimentações.\n" if not extrato else f"Extrato Bancário:\n{extrato}")
        print(f"Saldo Atual: R$ {saldo:.2f}")
        print("--"*20)
    elif opcao == 0:
        break
    else:
        print("Operação Inválida, Tente Novamente")
        print("--"*20)
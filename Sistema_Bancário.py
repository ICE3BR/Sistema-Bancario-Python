from abc import ABC, abstractmethod, abstractproperty
import datetime
import textwrap

class Cliente:
    def __init__(self, enderoco):
        self.enderoco = enderoco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, enderoco):
        super().__init__(enderoco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self._saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo: # Mensagem avisando: Saldo insuficiente
            print("\n@@@ Operação falhou! | Você não tem saldo suficiente. @@@")
            print(f"SALDO: R$ {saldo:.2f} | Valor Pedido de Saque: R$ {valor:.2f}")
        
        elif valor > 0: # Condição true para saque
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
            
        else:
            print("\n@@@ Operação falhou! | Valor inválido! @@@")
        return False

    def depositar(self, valor):
        if (valor > 0): # Condição True para deposito #
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else: # Condição False para deposito
            print("\n@@@ Operação falhou! | Valor inválido! @@@")
            print("--"*20)
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques
        
        if excedeu_limite:
            print("\n@@@ Operação falhou! | O valor do saque excede o limite. @@@")
            print(f"Limite disponível por saque: R$ {self.limite:.2f}")
            print(f"Valor Pedido: R$ {valor:.2f}")
        
        elif excedeu_saques:
            print("\n@@@ Operação falhou! | Número máximo de saques excedido. @@@")
            print(f"Os Limites de Saques mensais foram atingidos: {numero_saques}")
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agencia:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}    
        """

class Historico:
    def __init__(self): 
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        data = datetime.datetime.now().strftime("%d-%m-%Y|%H:%M:%S") # Corrigido %s para %S
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": data,
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """\n
☰☰☰☰☰☰☰☰ MENU ☰☰☰☰☰☰☰☰
[1]\tSacar
[2]\tDepositar 
[3]\tExtrato 
[4]\tNovo Usuário
[5]\tNova Conta
[6]\tListar Contas
[0]\tSair
=>> """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui contas cadastradas! @@@")
        return
    
    # FIXME: Não permite cliente escolher a conta
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    valor = float(input("Informe o valor de depósito: "))
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    valor = float(input("Informe o valor de saque: "))
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n=== Extrato ===\n")
    transacoes = conta.historico.transacoes
    
    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas Movimentações na conta."
    else:
        for transacao in transacoes:
            extrato += f"{transacao['data']}|\t{transacao['tipo']}: R${transacao['valor']:.2f}\n"
    
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print("\n=== Conta criada! ===")

def listar_contas(contas):
    for conta in contas:
        print("="*30)
        print(textwrap.dedent(str(conta)))

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente numeros): ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if cliente:
        print("\n @@@ Já existe cliente com esse CPF!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco =  input("Informe o endereco (logradouro, nro - bairro - cidade/silga estado): ")
    
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, enderoco=endereco)
    
    clientes.append(cliente)
    
    print("\n=== Cliente criado! ===")

def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == "1":
            sacar(clientes)
        elif opcao == "2":
            depositar(clientes)
        elif opcao == "3":
            exibir_extrato(clientes)
        elif opcao == "4":
            criar_cliente(clientes)
        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "6":
            listar_contas(contas)
        elif opcao == "0":
            break
        else:
            print("\n@@@ Operação inválida, tente novamente. @@@")

main()
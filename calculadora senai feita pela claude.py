"""
Calculadora SENAI 1.0
Módulo principal com operações matemáticas básicas e avançadas.
"""

import math


def exibir_menu():
    """Exibe o menu principal da calculadora."""
    print("\n[MENU] -> Selecione alguma das opções abaixo.")
    print("{1} Adição")
    print("{2} Subtração")
    print("{3} Multiplicação")
    print("{4} Divisão")
    print("{5} Potência")
    print("{6} Raiz Quadrada")
    print("{7} Porcentagem")
    print("{8} Fatorial")
    print("{9} AJUDA")
    print("{0} SAIR")


def obter_numeros(mensagem):
    """Solicita uma sequência de números separados por espaço e retorna uma lista de floats."""
    entrada = input(mensagem)
    return [float(n) for n in entrada.split()]


def calcular_adicao():
    """Realiza a soma de dois ou mais números."""
    numeros = obter_numeros("Informe os números que deseja somar: ")
    resultado = sum(numeros)
    print(f"O resultado da soma é = {resultado}")


def calcular_subtracao():
    """Realiza a subtração sequencial de dois ou mais números."""
    numeros = obter_numeros("Informe os números que deseja subtrair: ")
    resultado = numeros[0]
    for numero in numeros[1:]:
        resultado -= numero
    print(f"O resultado da subtração é = {resultado:.2f}")


def calcular_multiplicacao():
    """Realiza a multiplicação de dois ou mais números."""
    numeros = obter_numeros("Informe os números que deseja multiplicar: ")
    resultado = 1.0
    for numero in numeros:
        resultado *= numero
    print(f"O resultado da multiplicação é = {resultado:.2f}")


def calcular_divisao():
    """Realiza a divisão inteira e retorna o quociente e o resto."""
    numeros = obter_numeros("Informe os números que deseja dividir (dividendo divisor): ")

    if len(numeros) < 2:
        print("ERRO: Informe ao menos dois números.")
        return

    dividendo = numeros[0]
    divisor = numeros[1]

    if divisor == 0:
        print("ERRO: Divisão por zero não é permitida.")
        return

    quociente = dividendo // divisor
    resto = dividendo % divisor
    print(f"O quociente da divisão é {quociente:.2f} e o resto é {resto:.2f}")


def calcular_potencia():
    """Calcula a potenciação de uma base elevada a um expoente."""
    numeros = obter_numeros("Informe a base e o expoente separados por espaço: ")

    if len(numeros) < 2:
        print("ERRO: Informe a base e o expoente.")
        return

    base = numeros[0]
    expoente = numeros[1]
    resultado = base ** expoente
    print(f"O resultado de {base} elevado a {expoente} é = {resultado:.2f}")


def calcular_raiz_quadrada():
    """Calcula a raiz quadrada de um número."""
    numero = float(input("Informe o número para calcular a raiz quadrada: "))

    if numero < 0:
        print("ERRO: Não é possível calcular a raiz quadrada de um número negativo.")
        return

    resultado = math.sqrt(numero)
    print(f"A raiz quadrada de {numero} é = {resultado:.4f}")


def calcular_porcentagem():
    """Calcula a porcentagem de um valor."""
    percentual = float(input("Informe o valor da porcentagem (%): "))
    valor_base = float(input("Informe o número base: "))
    resultado = valor_base * (percentual / 100)
    print(f"{percentual}% de {valor_base} é = {resultado:.2f}")


def calcular_fatorial():
    """Calcula o fatorial de um número inteiro não negativo."""
    numero = int(input("Informe o número para calcular o fatorial: "))

    if numero < 0:
        print("ERRO: Fatorial não é definido para números negativos.")
        return

    resultado = math.factorial(numero)
    print(f"O fatorial de {numero} é = {resultado}")


def exibir_ajuda():
    """Exibe o menu de ajuda com informações sobre o uso da calculadora."""
    print("\n[AJUDA]")
    print("[1] Como usar a calculadora?")
    print("[2] Como voltar caso tenha executado o comando errado?")
    print("[3] As contas ficam salvas?")
    print("[4] Retornar à calculadora")

    opcoes_ajuda = {
        1: (
            "A calculadora opera com números separados por espaço.\n"
            "Exemplo para soma: digite '10 20 30' e o resultado será 60."
        ),
        2: "Funcionalidade em desenvolvimento.",
        3: "As contas não ficam salvas. Essa função pode ser adicionada em versões futuras.",
    }

    while True:
        try:
            opcao = int(input("\nEscolha uma opção: "))
        except ValueError:
            print("Entrada inválida. Digite um número.")
            continue

        if opcao == 4:
            print("Retornando à calculadora...")
            break
        elif opcao in opcoes_ajuda:
            print(opcoes_ajuda[opcao])
        else:
            print("Opção inválida. Tente novamente.")


# Mapeamento de opções para funções
OPERACOES = {
    1: calcular_adicao,
    2: calcular_subtracao,
    3: calcular_multiplicacao,
    4: calcular_divisao,
    5: calcular_potencia,
    6: calcular_raiz_quadrada,
    7: calcular_porcentagem,
    8: calcular_fatorial,
    9: exibir_ajuda,
}


def main():
    """Função principal que controla o loop da calculadora."""
    print("Bem-vindo à Calculadora 1.0.\n")
    exibir_menu()

    while True:
        try:
            escolha = int(input("\nInforme o número da operação desejada: "))
        except ValueError:
            print("Entrada inválida. Digite um número correspondente à operação.")
            continue

        if escolha == 0:
            print("\nSaindo da calculadora. Até logo!")
            break
        elif escolha in OPERACOES:
            OPERACOES[escolha]()
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
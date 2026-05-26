print("Bem vindo a Calculadora.\n")
print("[MENU] -> Selecione alguma das opções abaixo.")
print("{1} Adição.")
print("{2} Subtração.")
print("{3}")
print("{4}")
print("{5}")
print("{6}")
print("{7}")
print("{8}")
print("{9}")
print("{0}")
while True:
    escolha = int(input("Informe o número: "))
    if (escolha == 1):
        print("ADIÇÃO")
        numeros = str(input("Informe os numeros que deseja somar: "))
        lista_somativa = list(numeros.split(" "))
        soma = 0
        for numero in lista_somativa:
            soma += int(numero)
        print((f"o resultado da soma usando os numeros {numeros} é = {soma}"))
    if (escolha == 2):
        print("SUBTRAÇÃO ")
print("Bem vindo a Calculadora 1.0.\n")
print("[MENU] -> Selecione alguma das opções abaixo.")
print("{1} Adição.")
print("{2} Subtração.")
print("{3} Multiplicação")
print("{4} Divisão")
print("{5} Potência")
print("{6} Raiz Quadrada")
print("{7} Porcentagem")
print("{8} Fatorial")
print("{9} AJUDA")
print("{0} SAIR")
while True:
    escolha = int(input("Informe o número: "))
    if (escolha == 1):
        print("ADIÇÃO")
        numeros = str(input("Informe os numeros que deseja somar: "))
        lista_somativa = list(numeros.split(" "))
        soma = 0
        for numero in lista_somativa:
            soma += float(numero)
        print((f"o resultado da soma usando os numeros {numeros} é = {soma}"))
    if (escolha == 2):
        print("SUBTRAÇÃO")
        numero_sub = str(input("Informe os numeros que deseja subtrair: "))
        lista_subtrativa = list(numero_sub.split(" "))
        subtracao = float(lista_subtrativa[0])
        for i in range(1, len(lista_subtrativa)):
            subtracao -= float(lista_subtrativa[i])
        print(f"O resultado da subtração entre os valores {numero_sub} é igual a {subtracao:.2f}")
    if (escolha == 3):
        print("MULTIPLICAÇÃO")
        numeros_multi = str(input("Informe os números que deseja multiplicar: "))
        lista_multiplicativa = list(numeros_multi.split(" "))
        multiplicacao = 1
        for numeros_multi in lista_multiplicativa:
            multiplicacao *= float(numeros_multi)
        print(f"O resultado da multiplicação entre {numeros_multi} é igual a {multiplicacao:.2f}")
    if (escolha == 4):
        print("DIVISÃO")
        numeros_divis = str(input("Informe os numeros que deseja dividir: "))
        lista_divisiva = list(numeros_divis.split(" "))
        if lista_divisiva == 0:
            print("ERRO")
        else:
            divisao = float(lista_divisiva[0]) // float(lista_divisiva[1])
            resto = float(lista_divisiva[0]) % float(lista_divisiva[1])
        print(f"A divisão entre {numeros_divis} é igual a {divisao:.2f} e o seu resto é {resto:.2f} ")
    if (escolha == 5):
        print("POTÊNCIA")
        #numeros_potenciados = str(input("Informe o numero que deseja "))
        numero_base = float(input("Informe o numero que vai ser potenciado: "))
        potencia = int(input("Informe o expoente que vai ser utilizado no seu numero: "))
        potenciacao = (numero_base ** potencia)
        print(f"O resultado da potencia é {potenciacao}")
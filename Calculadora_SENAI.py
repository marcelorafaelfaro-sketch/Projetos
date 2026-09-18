from turtledemo.round_dance import stop

print("Bem vindo a Calculadora 1.0.\n")
nao = str
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

    escolha = int(input("Informe o número da operação que deseja realizar: "))
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
        numero_base = float(input("Informe o numero que vai ser potenciado: "))
        lista_potencia = list(numero_base.split(" "))
        potencia = float(lista_potencia[0]) ** float(lista_potencia[1])
        print(f"O resultado é {potencia:.2f}")
        #METODO ALTERNATIVO.
        # numeros_potenciados = str(input("Informe o numero que deseja "))
        #potencia = int(input("Informe o expoente que vai ser utilizado no seu numero: "))
        #potenciacao = (numero_base ** potencia)
        #print(f"O resultado da potencia é {potenciacao}")

    if (escolha == 6):
        print("RAIZ QUADRADA")
        numero_raiz = int(input("Informe o numero que você deseja ter a raiz quadrada: "))
        #lista_raiz = list(numero_raiz.split(" "))
        #resultado_raiz = int((lista_raiz ** 0.5))
        import math
        resultado = math.sqrt(numero_raiz)
        print(f"O resultado da raiz quadrada de {numero_raiz} é igual a {resultado}")

    if (escolha == 7):
       print("PORCENTAGEM")
       # numero_porcento = str(input("Informe a porcentagem e o valor que será usado, respectivamente: "))
       # lista_porcento = list(numero_porcento.split(" "))
       # porcentagem = (int(lista_porcento[0]) * int(lista_porcento[1]/100))
       # print(f"O resultado é {porcentagem}")
       porcentagem2_extra = float(input("Informe o número da porcentagem: "))
       numero_porcentado = float(input("Informe o número: "))
       conta_porcento = numero_porcentado * (porcentagem2_extra/100)
       print(f"O resultado de {porcentagem2_extra}% de {numero_porcentado} é igual a {conta_porcento}")

    if (escolha == 8):
        print("FATORIAL")
        a_ser_fatoriado = int(input("Informe o número que você deseja ter o fatorial: "))
        resultado_fatorial = 1
        for i in range(a_ser_fatoriado,0, -1):
            resultado_fatorial = resultado_fatorial * i
            #print (f"{resultado_fatorial} * i")
        print(f"O fatorial de {a_ser_fatoriado} é igual a {resultado_fatorial}")

    if (escolha == 0):
        print("""
        
        SAINDO DA CALCULADORA 
        
        """)
        break

    else:
        print(""" 
        
    
        
              SIXXXX SEVEN    
        
        
        
        
        """)

    if (escolha == 9):
        print("AJUDA")
        print(("""
        
                [1]- COMO USAR A CALCULADORA?
                [2]- COMO VOLTAR CASO TENHA EXECUTADO O COMANDO ERRADO
                [3]- AS CONTAS FICAM SALVAS?
                [4]- RETORNAR A CALCULADORA
         
         
         
         """))
        while True:
            escolha_da_opcao9 = int(input("Escolha a opção: "))
            if (escolha_da_opcao9 == 1):
                print("A calculadora opera utilizando uma linha de codigo, ou seja, na soma e nas demais funções você\n "
                      "digita um valor logo em seguida do outro, os separando com espaços.\n"
                      "EX:(Digite a opção da soma) SOMA 10 10.\n O resultado que irá aparecer é 20 ")
            elif (escolha_da_opcao9 == 4):
                print("Retornando ao início.")
                break
            elif (escolha_da_opcao9 == 2):
                print("EM DESENVOLVIMENTO AINDA")
            elif (escolha_da_opcao9 == 3):
                print("Infelizmente as contas não ficam salvas, talvez nas próximas atualizações tenha essa função.")







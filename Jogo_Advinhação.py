import random
import os
#jogo da advinhação
novo_jogo = "s"
while novo_jogo == "s":
    print('''               
         BEM VINDO AO JOGO DA ADVINHAÇÃO\n''')
    numero = random.randint(1,3)
    print("Nesse jogo você terá que advinhar o número correto entre 1 e 15")
    print("Você terá 3 chances, irei dizer se o numero é maior ou menor")
    for i in range(3):
        chute = int(input("Informe o número que você acha que estou pensando: "))
        if chute == numero:
            print("Parabéns")
            break
        elif chute > numero:
            print("O numero que estou pensando é um pouco menor")
        elif chute < numero:
            print("O numero que estou pensando é um pouco maior")

    if chute != numero:
        print(f"O número que eu estava pensando é: {numero}")
        novo_jogo = input(f"Deseja jogar de novo? Se sim, tecle S, caso não, tecle qualquer outra tecla: ")
        novo_jogo = novo_jogo.lower()
        os.system("clear")
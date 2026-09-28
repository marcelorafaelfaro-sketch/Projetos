import mysql.connector


    # conectado = mysql.connector.connect(
    #     host= "localhost",
    #     user= "root",
    #     password= "root",
    #     database= "db_gerenciador_de_tarefas"
    # )
    # mouse = conectado.cursor()
    # comando = "SELECT id, titulo, status, data_criacao FROM tarefas;"
    # mouse.execute(comando)
    # print("\n --Lista de tarefas (Mysql + python )---")
    # resultado = mouse.fetchall()
    # for tarefa in resultado:
    #     print(f"ID {tarefa[0]}| Título: {tarefa[1]} | Status: {tarefa[2]} | Data: {tarefa[3]}")
    #
    # mouse.close()
    # conectado.close()

#começa aqui o "meu coodigo"
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="db_gerenciador_de_tarefas"
    )


def listar_de_tarefas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, titulo, status, data_criacao FROM tarefas;")
    resultados = cursor.fetchall()

    print("\n-- LISTA DE TAREFAS ---")
    if not resultados:
        print("Nenhuma tarefa encontrada.")
    else:
        for t in resultados:
            print(
                f"ID: {t[0]} | Título: {t[1]} | Status: {t[2]} | Data: {t[3]}"
            )
    cursor.close()
    conexao.close()

def adicionar_tarefa(titulo):
    conexao = conectar()
    cursor = conexao.cursor()
    # Usamos CURDATE() para inserir a data atual automaticamente
    comando = "INSERT INTO tarefas (titulo, status, data_criacao) VALUES (%s, %s, CURDATE())"
    cursor.execute(comando, (titulo, "Em andamento"))
    conexao.commit()  # Confirma as alterações na base de dados
    print("✅ Tarefa adicionada com sucesso!")
    cursor.close()
    conexao.close()

def concluir_tarefa(id_tarefa):
    conexao = conectar()
    cursor = conexao.cursor()
    comando = "UPDATE tarefas SET status = 'Concluída' WHERE id = %s"
    cursor.execute(comando, (id_tarefa,))
    conexao.commit()
    print("✅ Tarefa marcada como concluída!")
    cursor.close()
    conexao.close()

def apagar_tarefa(id_tarefa):
    conexao = conectar()
    cursor = conexao.cursor()
    comando = "DELETE FROM tarefas WHERE id = %s"
    cursor.execute(comando, (id_tarefa,))
    conexao.commit()
    print("🗑️ Tarefa removida com sucesso!")
    cursor.close()
    conexao.close()

    # Menu Principal
while True:
    print("\n=== GERENCIADOR DE TAREFAS ===")
    print("1. Listar tarefas")
    print("2. Adicionar tarefa")
    print("3. Concluir tarefa")
    print("4. Apagar tarefa")
    print("5. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        listar_de_tarefas()
    elif opcao == "2":
        titulo = input("Digite o título da tarefa: ")
        adicionar_tarefa(titulo)
    elif opcao == "3":
        id_t = input("Digite o ID da tarefa a concluir: ")
        concluir_tarefa(id_t)
    elif opcao == "4":
        id_t = input("Digite o ID da tarefa a apagar: ")
        apagar_tarefa(id_t)
    elif opcao == "5":
        print("Programa encerrado!")
        break
    else:
        print("Opção inválida! Tente novamente.")



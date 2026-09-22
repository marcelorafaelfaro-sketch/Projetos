import mysql.connector


conectado = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password= "root",
    database= "db_gerenciador_de_tarefas"
)
mouse = conectado.cursor()
comando = "SELECT id, titulo, status, data_criacao FROM tarefas;"
mouse.execute(comando)
print("\n --Lista de tarefas (Mysql + python )---")
resultado = mouse.fetchall()
for tarefa in resultado:
    print(f"ID {tarefa[0]}| Título: {tarefa[1]} | Status: {tarefa[2]} | Data: {tarefa[3]}")

mouse.close()
conectado.close()

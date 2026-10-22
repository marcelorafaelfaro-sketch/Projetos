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
# def conectar():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="root",
#         database="db_gerenciador_de_tarefas"
#     )
#
#
# def listar_de_tarefas():
#     conexao = conectar()
#     cursor = conexao.cursor()
#     cursor.execute("SELECT id, titulo, status, data_criacao FROM tarefas;")
#     resultados = cursor.fetchall()
#
#     print("\n-- LISTA DE TAREFAS ---")
#     if not resultados:
#         print("Nenhuma tarefa encontrada.")
#     else:
#         for t in resultados:
#             print(
#                 f"ID: {t[0]} | Título: {t[1]} | Status: {t[2]} | Data: {t[3]}"
#             )
#     cursor.close()
#     conexao.close()
#
# def adicionar_tarefa(titulo):
#     conexao = conectar()
#     cursor = conexao.cursor()
#     # Usamos CURDATE() para inserir a data atual automaticamente
#     comando = "INSERT INTO tarefas (titulo, status, data_criacao) VALUES (%s, %s, CURDATE())"
#     cursor.execute(comando, (titulo, "Em andamento"))
#     conexao.commit()  # Confirma as alterações na base de dados
#     print("✅ Tarefa adicionada com sucesso!")
#     cursor.close()
#     conexao.close()
#
# def concluir_tarefa(id_tarefa):
#     conexao = conectar()
#     cursor = conexao.cursor()
#     comando = "UPDATE tarefas SET status = 'Concluída' WHERE id = %s"
#     cursor.execute(comando, (id_tarefa,))
#     conexao.commit()
#     print("✅ Tarefa marcada como concluída!")
#     cursor.close()
#     conexao.close()
#
# def apagar_tarefa(id_tarefa):
#     conexao = conectar()
#     cursor = conexao.cursor()
#     comando = "DELETE FROM tarefas WHERE id = %s"
#     cursor.execute(comando, (id_tarefa,))
#     conexao.commit()
#     print("🗑️ Tarefa removida com sucesso!")
#     cursor.close()
#     conexao.close()
#
#     # Menu Principal
# while True:
#     print("\n=== GERENCIADOR DE TAREFAS ===")
#     print("1. Listar tarefas")
#     print("2. Adicionar tarefa")
#     print("3. Concluir tarefa")
#     print("4. Apagar tarefa")
#     print("5. Sair")
#
#     opcao = input("Escolha uma opção: ")
#
#     if opcao == "1":
#         listar_de_tarefas()
#     elif opcao == "2":
#         titulo = input("Digite o título da tarefa: ")
#         adicionar_tarefa(titulo)
#     elif opcao == "3":
#         id_t = input("Digite o ID da tarefa a concluir: ")
#         concluir_tarefa(id_t)
#     elif opcao == "4":
#         id_t = input("Digite o ID da tarefa a apagar: ")
#         apagar_tarefa(id_t)
#     elif opcao == "5":
#         print("Programa encerrado!")
#         break
#     else:
#         print("Opção inválida! Tente novamente.")
#
#--------------- versao gemini/CLAUDE pro linux----------------------





import sqlite3
from contextlib import closing
from pathlib import Path

import customtkinter as ctk

ctk.set_appearance_mode("System")  # Segue o tema (claro/escuro) do sistema
ctk.set_default_color_theme("blue")

# Pasta fixa do usuário: funciona em Linux e Windows, e continua funcionando
# depois de virar .exe (não depende de onde o script/executável está).
PASTA_DADOS = Path.home() / ".gerenciador_tarefas"
BANCO_PATH = PASTA_DADOS / "agenda.db"

STATUS_ANDAMENTO = "Em andamento"
STATUS_CONCLUIDA = "Concluída"


# ---------------------------------------------------------------- BANCO ----
def conectar():
    PASTA_DADOS.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(BANCO_PATH)


def executar(sql, params=()):
    """Roda um comando que altera dados e já confirma (commit)."""
    with closing(conectar()) as conexao:
        with conexao:
            conexao.execute(sql, params)


def consultar(sql, params=()):
    with closing(conectar()) as conexao:
        return conexao.execute(sql, params).fetchall()


def criar_tabela():
    executar(
        """
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            status TEXT NOT NULL,
            data_criacao TEXT NOT NULL
        )
        """
    )


def listar_tarefas():
    return consultar(
        "SELECT id, titulo, status, data_criacao FROM tarefas "
        "ORDER BY (status = ?), id DESC",  # pendentes primeiro, mais novas no topo
        (STATUS_CONCLUIDA,),
    )


def inserir_tarefa(titulo):
    # 'localtime' garante a data do seu fuso, e não a data em UTC
    executar(
        "INSERT INTO tarefas (titulo, status, data_criacao) "
        "VALUES (?, ?, DATE('now', 'localtime'))",
        (titulo, STATUS_ANDAMENTO),
    )


def alternar_status(id_tarefa):
    executar(
        "UPDATE tarefas SET status = CASE WHEN status = ? THEN ? ELSE ? END "
        "WHERE id = ?",
        (STATUS_CONCLUIDA, STATUS_ANDAMENTO, STATUS_CONCLUIDA, id_tarefa),
    )


def apagar_tarefa(id_tarefa):
    executar("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))


def formatar_data(data_iso):
    """'2026-10-22' -> '22/10/2026'"""
    try:
        ano, mes, dia = data_iso.split("-")
        return f"{dia}/{mes}/{ano}"
    except ValueError:
        return data_iso


# ------------------------------------------------------------ INTERFACE ----
class AppAgenda(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Tarefas")
        self.geometry("1920x1080")#TAMANHO ORIGINAL 520x640
        self.resizable(False, False)

        criar_tabela()

        # Título
        ctk.CTkLabel(
            self, text="Minhas Tarefas", font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(20, 5))

        # Contador de pendentes
        self.label_contador = ctk.CTkLabel(self, text="", text_color="gray50")
        self.label_contador.pack()

        # Campo + botão de adicionar
        barra = ctk.CTkFrame(self, fg_color="transparent")
        barra.pack(pady=(15, 0), padx=20, fill="x")
        barra.grid_columnconfigure(0, weight=1)

        self.entry_tarefa = ctk.CTkEntry(
            barra, placeholder_text="Digite o título da tarefa e aperte Enter..."
        )
        self.entry_tarefa.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.entry_tarefa.bind("<Return>", lambda _evento: self.adicionar_tarefa())

        ctk.CTkButton(
            barra, text="Adicionar", width=90, command=self.adicionar_tarefa
        ).grid(row=0, column=1)

        # Aviso de erro (some sozinho depois de 2 segundos)
        self.label_aviso = ctk.CTkLabel(self, text="", text_color="#e5484d", height=18)
        self.label_aviso.pack(pady=(4, 0))

        # Lista rolável de tarefas
        self.frame_lista = ctk.CTkScrollableFrame(self)
        self.frame_lista.pack(padx=20, pady=(5, 20), fill="both", expand=True)

        self.entry_tarefa.focus()
        self.atualizar_lista()

    # ---- ações ----
    def adicionar_tarefa(self):
        titulo = self.entry_tarefa.get().strip()
        if not titulo:
            self.mostrar_aviso("Digite um título para a tarefa.")
            return
        inserir_tarefa(titulo)
        self.entry_tarefa.delete(0, "end")
        self.atualizar_lista()

    def alternar(self, id_tarefa):
        alternar_status(id_tarefa)
        self.atualizar_lista()

    def apagar(self, id_tarefa):
        apagar_tarefa(id_tarefa)
        self.atualizar_lista()

    def mostrar_aviso(self, texto):
        self.label_aviso.configure(text=texto)
        self.after(2000, lambda: self.label_aviso.configure(text=""))

    # ---- desenho da lista ----
    def atualizar_lista(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        tarefas = listar_tarefas()
        pendentes = sum(1 for t in tarefas if t[2] != STATUS_CONCLUIDA)
        self.label_contador.configure(
            text=f"{pendentes} pendente(s) de {len(tarefas)} no total"
        )

        if not tarefas:
            ctk.CTkLabel(
                self.frame_lista, text="Nenhuma tarefa cadastrada.", text_color="gray50"
            ).pack(pady=30)
            return

        for id_tarefa, titulo, status, data in tarefas:
            self.criar_linha(id_tarefa, titulo, status == STATUS_CONCLUIDA, data)

    def criar_linha(self, id_tarefa, titulo, concluida, data):
        linha = ctk.CTkFrame(self.frame_lista)
        linha.pack(fill="x", padx=2, pady=4)
        linha.grid_columnconfigure(0, weight=1)

        cor_texto = "gray50" if concluida else None
        fonte = ctk.CTkFont(size=14, overstrike=concluida)  # riscado se concluída

        ctk.CTkLabel(
            linha,
            text=titulo,
            font=fonte,
            text_color=cor_texto,
            anchor="w",
            justify="left",
            wraplength=250,
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(8, 0))

        ctk.CTkLabel(
            linha,
            text=f"Criada em {formatar_data(data)}",
            font=ctk.CTkFont(size=11),
            text_color="gray50",
            anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=10, pady=(0, 8))

        ctk.CTkButton(
            linha,
            text="Reabrir" if concluida else "Concluir",
            width=80,
            fg_color="gray40" if concluida else "#2f9e44",
            hover_color="gray30" if concluida else "#237a34",
            command=lambda i=id_tarefa: self.alternar(i),
        ).grid(row=0, column=1, rowspan=2, padx=(0, 6))

        ctk.CTkButton(
            linha,
            text="Apagar",
            width=70,
            fg_color="#e5484d",
            hover_color="#b83a3e",
            command=lambda i=id_tarefa: self.apagar(i),
        ).grid(row=0, column=2, rowspan=2, padx=(0, 10))


if __name__ == "__main__":
    app = AppAgenda()
    app.mainloop()

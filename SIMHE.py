import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import numpy as np
import webbrowser

import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# =========================
# LEITURA DAS PLANILHAS
# =========================

from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Esconde a janela principal do Tkinter
Tk().withdraw()

print("Selecione a planilha de qualidade da água")

arquivo_agua = askopenfilename(
    title="Selecione a planilha de qualidade da água",
    filetypes=[
        ("Arquivos CSV", "*.csv"),
        ("Arquivos Excel", "*.xlsx")
    ]
)

print("Selecione a planilha de doenças")

arquivo_doencas = askopenfilename(
    title="Selecione a planilha de doenças",
    filetypes=[
        ("Arquivos CSV", "*.csv"),
        ("Arquivos Excel", "*.xlsx")
    ]
)

# Leitura da planilha de água

if arquivo_agua.endswith(".csv"):
    agua = pd.read_csv(arquivo_agua)
else:
    agua = pd.read_excel(arquivo_agua)

# Leitura da planilha de doenças

if arquivo_doencas.endswith(".csv"):
    doencas = pd.read_csv(arquivo_doencas)
else:
    doencas = pd.read_excel(arquivo_doencas)

# =========================
# JUNÇÃO DOS DADOS
# =========================

dados = pd.merge(agua, doencas, on='bairro')

FATOR_POPULACIONAL = 10000

dados['taxa_dengue'] = (
    dados['dengue'] /
    dados['populacao']
) * FATOR_POPULACIONAL

dados['taxa_leptospirose'] = (
    dados['leptospirose'] /
    dados['populacao']
) * FATOR_POPULACIONAL

dados['taxa_diarreia'] = (
    dados['diarreia'] /
    dados['populacao']
) * FATOR_POPULACIONAL

# =========================
# CÁLCULO DE RISCO
# =========================

def calcular_risco(linha):
    risco = 0

    # Água
    if linha['ph'] < 6.5:
        risco += 2

    if linha['turbidez_ntu'] > 5:
        risco += 2

    if linha['coliformes_npm100ml'] > 100:
        risco += 3

    if linha['nitrato_mgl'] > 10:
        risco += 2

    # Doenças
    risco += linha['taxa_dengue'] * 0.15
    risco += linha['taxa_leptospirose'] * 0.30
    risco += linha['taxa_diarreia'] * 0.10
    return risco


dados['indice_risco'] = dados.apply(calcular_risco, axis=1)

# =========================
# CLASSIFICAÇÃO
# =========================

def classificar(valor):
    if valor < 5:
        return 'BAIXO'
    elif valor < 10:
        return 'MÉDIO'
    else:
        return 'ALTO'


dados['classificacao'] = dados['indice_risco'].apply(classificar)

# =========================
# EXIBIÇÃO DOS RESULTADOS
# =========================

print('\n===== RELATÓRIO =====\n')
print(dados[['bairro', 'indice_risco', 'classificacao']])

# =========================
# RANKING DAS ÁREAS
# =========================

ranking = dados.sort_values(by='indice_risco', ascending=False)

print('\n===== ÁREAS MAIS CRÍTICAS =====\n')
print(ranking[['bairro', 'indice_risco']])

# =========================
# GRÁFICO DE RISCO
# =========================

plt.figure(figsize=(10,6))
sns.barplot(x='bairro', y='indice_risco', data=ranking)
plt.title('Índice de Risco por Bairro')
plt.xlabel('Bairro')
plt.ylabel('Risco')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show(block=False)

# =========================
# MAPA INTERATIVO
# =========================

mapa = folium.Map(location=[-1.45, -48.49], zoom_start=12)

for _, linha in dados.iterrows():

    if linha['classificacao'] == 'ALTO':
        cor = 'red'
    elif linha['classificacao'] == 'MÉDIO':
        cor = 'orange'
    else:
        cor = 'green'

    texto = f'''
    <b>Bairro:</b> {linha['bairro']}<br>

    <b>Índice de risco:</b> {linha['indice_risco']:.2f}<br>

    <b>Classificação:</b> {linha['classificacao']}<br><br>

    <b>População:</b> {linha['populacao']:,}<br><br>

    <b>Dengue:</b><br>
    {linha['dengue']} casos<br>
    {linha['taxa_dengue']:.2f} casos por 10 mil habitantes<br><br>

    <b>Leptospirose:</b><br>
    {linha['leptospirose']} casos<br>
    {linha['taxa_leptospirose']:.2f} casos por 10 mil habitantes<br><br>

    <b>Diarreia:</b><br>
    {linha['diarreia']} casos<br>
    {linha['taxa_diarreia']:.2f} casos por 10 mil habitantes<br><br>

    <b>Qualidade da Água</b><br>

    pH: {linha['ph']}<br>
    Turbidez: {linha['turbidez_ntu']} NTU<br>
    Coliformes: {linha['coliformes_npm100ml']} NMP/100mL<br>
    Nitrato: {linha['nitrato_mgl']} mg/L
    '''

    folium.CircleMarker(
        location=[linha['latitude'], linha['longitude']],
        radius=10,
        popup=texto,
        color=cor,
        fill=True,
        fill_color=cor,
        fill_opacity=0.7
    ).add_to(mapa)

# Salvar mapa
mapa.save('mapa_risco.html')
webbrowser.open("mapa_risco.html")

print('\nMapa salvo como mapa_risco.html')

# =========================
# DETECÇÃO DO EPICENTRO
# =========================

epicentro = dados.loc[dados['indice_risco'].idxmax()]

print('\n===== EPICENTRO DETECTADO =====\n')
print(f"Bairro: {epicentro['bairro']}")
print(f"Índice de risco: {epicentro['indice_risco']:.2f}")
print(f"Classificação: {epicentro['classificacao']}")

# =========================
# JANELA VISUAL DE RESULTADOS
# =========================

janela = tk.Tk()

janela.iconbitmap("iconeSIMHE.ico")

janela.title(
    "Sistema Inteligente de Monitoramento Hídrico e Epidemiológico"
)

janela.geometry("800x700")

texto = ScrolledText(
    janela,
    width=120,
    height=40,
    font=("Arial", 11)
)

texto.pack(
    padx=10,
    pady=10,
    fill="both",
    expand=True
)

relatorio = ""

relatorio += (
    "=====================================\n"
    "SISTEMA INTELIGENTE DE MONITORAMENTO HÍDRICO E EPIDEMIOLÓGICO\n"
    "=====================================\n\n"
)

# Epicentro

relatorio += (
    "EPICENTRO DETECTADO\n"
    "---------------------\n"
)

relatorio += (
    f"Bairro: {epicentro['bairro']}\n"
)

relatorio += (
    f"Índice de risco: "
    f"{epicentro['indice_risco']:.2f}\n"
)

relatorio += (
    f"Classificação: "
    f"{epicentro['classificacao']}\n\n"
)

# Ranking

relatorio += (
    "RANKING DE RISCO\n"
    "---------------------\n\n"
)

for posicao, (_, linha) in enumerate(
        ranking.iterrows(),
        start=1):

    relatorio += (
        f"{posicao}º Lugar\n"
        f"Bairro: {linha['bairro']}\n"
        f"Índice de risco: "
        f"{linha['indice_risco']:.2f}\n"
        f"Classificação: "
        f"{linha['classificacao']}\n\n"
    )

# Alertas

relatorio += (
    "\nALERTAS AUTOMÁTICOS\n"
    "---------------------\n\n"
)

for _, linha in dados.iterrows():

    if linha['classificacao'] == 'ALTO':

        relatorio += (
            f"ALERTA: "
            f"{linha['bairro']} "
            f"apresenta ALTO RISCO\n"
        )

texto.insert(
    tk.END,
    relatorio
)

texto.config(
    state='disabled'
)

# =========================
# ALERTA AUTOMÁTICO
# =========================

print('\n===== ALERTAS =====\n')

for _, linha in dados.iterrows():
    if linha['classificacao'] == 'ALTO':
        print(f"ALERTA: {linha['bairro']} apresenta alto risco!")
janela.mainloop()





#teste

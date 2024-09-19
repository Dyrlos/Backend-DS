import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.gridspec import GridSpec
from datetime import datetime
from psycopg2 import sql
from sqlalchemy import create_engine

#Criando engine para conectar no banco
engine = create_engine('postgresql+psycopg2://postgres:#abc123#@localhost:5432/forum') 
#Querys de consultas
query_funcionarios = "SELECT * FROM funcionarios;" 
query_tarefas = "SELECT * FROM tarefas;"
#Lendo e criando DataFrame com a query de funcionarios
df_funcionarios = pd.read_sql(query_funcionarios, engine)
#Criando coluna Idade aplicando função para calcular a data de hoje - data de nascimento
hoje = datetime.now() 
df_funcionarios['idade'] = df_funcionarios['data_nascimento'].apply(lambda data: hoje.year - data.year - ((hoje.month, hoje.day) < (data.month, data.day)))
#Salvando as informações do DataFrame Funcionarios em um arquivo Excel
df_funcionarios.to_excel('df_funcionarios.xlsx', index=False)
#Lendo e criando DataFrame com a query de Tarefas
df_tarefas = pd.read_sql(query_tarefas, engine)
#Alterando os valores de status e prioridade das tarefas para String
df_tarefas['status'] = df_tarefas['status'].replace({0: 'A fazer', 1: 'Em progresso', 2: 'Concluído'})
df_tarefas['prioridade'] = df_tarefas['prioridade'].replace({0: 'Alta', 1: 'Média', 2: 'Baixa'})
#Salvando as informações do DataFrame Tarefas em um arquivo Excel
df_tarefas.to_excel('df_tarefas.xlsx', index=False)
#Contagens necessárias para os gráficos
contagem_cargo = df_funcionarios['cargo'].value_counts()
contagem_idade = df_funcionarios['idade'].value_counts().sort_index(ascending=True)
contagem_sexo = df_funcionarios['sexo'].value_counts()
contagem_status = df_tarefas['status'].value_counts()
contagem_prioridade = df_tarefas['prioridade'].value_counts()

#Função para colocar os textos em negrito com tamanho 12
def fonte_negrito():
    for autotext in autotexts:
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')

    for text in texts:
        text.set_fontsize(12)
        text.set_fontweight('bold')
#Função para criar o dashboard
def gera_dashboard(df_funcionarios):
    #Criação da figura e layout
    fig = plt.figure(figsize=(20, 10), facecolor='black')
    #Definindo a grade 3x2
    gs = GridSpec(3, 2, height_ratios=[1, 0.6, 1], width_ratios=[1, 1])
    #Titulo do dashboard
    fig.suptitle('Dashboard de Dados da Empresa', fontsize=24, color='white', y=1.0)

    # Gráfico 1 - Contagem por cargo
    ax1 = plt.subplot(gs[0, 0])
    sns.barplot(x=contagem_cargo.index, y=contagem_cargo.values, hue=contagem_cargo.index, palette='crest_r', ax=ax1, legend=False)
    ax1.set_xlabel('Cargo', color='white')
    ax1.set_ylabel('Contagem', color='white')
    ax1.set_title('Contagem de Pessoas por Cargo', color='white')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax1.set_ylim(0, contagem_cargo.max() + (contagem_cargo.max() / 10))
    #Atribuindo os valores acima de cada barra vertical
    for i, valor in enumerate(contagem_cargo):
        ax1.text(i, valor + 0.5, f'{valor}', ha='center', va='bottom', color='black')

    # Gráfico 2 - Contagem por sexo
    ax2 = plt.subplot(gs[0, 1])
    colors = sns.color_palette("crest_r")
    rotulos = ['Masculino', 'Feminino']
    legenda = [f'{rotulos[i]}: {contagem_sexo[i]}' for i in range(len(rotulos))]
    wedges, texts, autotexts = ax2.pie(contagem_sexo,
                                      labels=rotulos,
                                      textprops={'color': 'white'},
                                      autopct='%1.1f%%',
                                      startangle=90,
                                      colors=colors)
    ax2.set_title('Contagem de Sexo por Funcionarios', color='white', fontsize=16)
    ax2.axis('equal')
    ax2.legend(legenda, loc='upper left', bbox_to_anchor=(0.8, 0.97), facecolor='white', edgecolor='lightgrey', fontsize=12, title_fontsize='13', shadow=True)
    fonte_negrito()
    
    # Gráfico 3 - Contagem por idade
    ax3 = plt.subplot(gs[1, :])
    sns.barplot(x=contagem_idade.index, y=contagem_idade.values, hue=contagem_idade.index, palette='crest', ax=ax3, legend=False)
    ax3.set_xlabel('Idade', color='white')
    ax3.set_title('Contagem de Idade por Funcionarios', color='white')
    ax3.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax3.tick_params(axis='x', colors='white')
    ax3.tick_params(axis='y', colors='white')
    ax3.set_ylim(0, contagem_idade.max() + (contagem_idade.max() * 0.10))
    ax3.set_yticklabels([])

    for p in ax3.patches:
        height = p.get_height()
        ax3.text(x=p.get_x() + p.get_width() / 2,
                 y=height + 0.1,  # Posição ligeiramente acima da barra
                 s=f'{int(height)}',  # Valor da contagem
                 ha='center', color='black')  # Centralizar o texto

    #Gráfico 4 - Contagem Status
    ax4 = plt.subplot(gs[2, 0])
    colors = sns.color_palette("crest_r")
    rotulos = ['A fazer', 'Em progresso', 'Concluído']
    legenda = [f'{rotulos[i]}: {contagem_status[i]}' for i in range(len(rotulos))]
    wedges, texts, autotexts = ax4.pie(contagem_status,
                                      labels=rotulos,
                                      textprops={'color': 'white'},
                                      autopct='%1.1f%%',
                                      startangle=90,
                                      colors=colors)
    ax4.set_title('Contagem de Status de Tarefas', color='white', fontsize=16)
    ax4.axis('equal')
    ax4.legend(legenda, loc='upper left', bbox_to_anchor=(0.8, 0.97), facecolor='white', edgecolor='lightgrey', fontsize=12, title_fontsize='13', shadow=True)
    fonte_negrito()
    
    #Gráfico 5 - Contagem Prioridade
    ax5 = plt.subplot(gs[2, 1])
    colors = sns.color_palette("crest_r")
    rotulos = ['Alta', 'Média', 'Baixa']
    legenda = [f'{rotulos[i]}: {contagem_prioridade[i]}' for i in range(len(rotulos))]
    wedges, texts, autotexts = ax5.pie(contagem_prioridade,
                                      labels=rotulos,
                                      textprops={'color': 'white'},
                                      autopct='%1.1f%%',
                                      startangle=90,
                                      colors=colors)
    ax5.set_title('Contagem de Prioridade por Tarefas', color='white', fontsize=16)
    ax5.axis('equal')
    ax5.legend(legenda, loc='upper left', bbox_to_anchor=(0.8, 0.97), facecolor='white', edgecolor='lightgrey', fontsize=12, title_fontsize='13', shadow=True)
    fonte_negrito()
    
    #Ajustando o layout do dashboard e salva o gráfico como uma imagem png
    plt.tight_layout()
    plt.savefig('dashboard.png', facecolor=fig.get_facecolor())

    #Salvando em HTML
    html_content = f"""
        <html>
            <head>
                <title>Dashboard</title>
                <style>
                    body {{
                        background-color: black;
                        color: white;
                    }}
                    img {{
                        display: block;
                        margin-left: auto;
                        margin-right: auto;
                    }}
                </style>
            </head>
            <body>
                <img src="dashboard.png" alt="Dashboard">
            </body>
        </html>
        """
    with open("dashboard.html", "w") as file:
        file.write(html_content)

    #Apresentando o dashboard
    plt.show()

cria_grafico(df_funcionarios)

engine.dispose()

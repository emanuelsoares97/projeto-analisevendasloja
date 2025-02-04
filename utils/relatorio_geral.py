import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utils.merge_tabelas import merge_tabelas
from utils.logger_utils import get_logger
from classes.classanaliselojas import AnaliseLojas 
from classes.classanaliseatendentes import AnaliseAtendentes
from classes.classanalisevendas import AnaliseVendas
from datetime import datetime

# Configurar logger
logger = get_logger("Relatorio Final")

def gerar_relatorio(db_manager):
    """
    Gera um relatório final com os principais indicadores de vendas.
    """
    logger.info("Iniciando geração do relatório consolidado.")

    # Criar pasta para os gráficos
    caminho_graficos = "graficos/relatorio"
    os.makedirs(caminho_graficos, exist_ok=True)

    # Criar instâncias das classes de análise
    analise_lojas = AnaliseLojas(db_manager)
    analise_atendentes = AnaliseAtendentes(db_manager)
    analise_vendas = AnaliseVendas(db_manager)

    # Ticket Médio por Loja e Atendente
    df_ticket_loja = analise_lojas.media_ticket_loja()  # Método já salva CSV
    df_ticket_atendente = analise_atendentes.atendentes_ticket_medio_venda()  # Método já salva CSV

    # Top 10 Produtos Mais Vendidos
    df_top_produtos = analise_vendas.calcular_produtos_mais_vendidos()

    # Faturamento Total por Loja e Atendente
    df_faturamento_loja = analise_lojas.total_faturado_por_loja()
    df_faturamento_atendente = analise_atendentes.atendentes_mais_faturaram()  

    # Evolução das Vendas ao Longo do Tempo ano atual
    df_vendas_tempo = analise_vendas.calcular_total_vendas_mes()
    

    #  Gerar Gráficos
    plt.figure(figsize=(12, 6))
    plt.bar(df_faturamento_loja["Loja"], df_faturamento_loja["Receita Total"], color='blue')
    plt.xticks(rotation=45)
    plt.title("Faturamento Total por Loja")
    plt.ylabel("Receita Total")      
    plt.savefig(os.path.join(caminho_graficos, "faturamento_loja.png"))
    plt.close()

    plt.figure(figsize=(12, 6))
    plt.bar(df_top_produtos["Produto"], df_top_produtos["Quantidade"], color='green')
    plt.xticks(rotation=45)
    plt.title("Top 10 Produtos Mais Vendidos")
    plt.ylabel("Quantidade Vendida")
    plt.savefig(os.path.join(caminho_graficos, "top_produtos.png"))
    plt.close()

    plt.figure(figsize=(12, 6))
    plt.plot(df_vendas_tempo["Data"], df_vendas_tempo["Receita Total"], marker='o', linestyle='-')
    plt.title(f"Evolução das Vendas ao Longo do Tempo ({df_vendas_tempo['Data'].iloc[0][:4]})")  # Ano mais recente no título
    plt.ylabel("Receita Total")
    plt.xlabel("Data")
    plt.xticks(rotation=45)
    plt.grid()
    plt.savefig(os.path.join(caminho_graficos, "evolucao_vendas.png"))
    plt.close()

    logger.info("Relatório gerado com sucesso.")

if __name__ == "__main__":
    from classes.classdatabasemanager import DatabaseManager
    db_manager = DatabaseManager()
    gerar_relatorio(db_manager)

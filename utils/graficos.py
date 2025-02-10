import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker
from datetime import datetime
from utils.logger_utils import get_logger

sns.set_theme(style="whitegrid")
logger = get_logger("GeradorGraficos")

def gerar_grafico_barras(df, titulo, xlabel, ylabel, nome_ficheiro="grafico"):
    """
    Gera um gráfico de barras usando Seaborn e salva a imagem gerada.

    :param df: DataFrame contendo os dados para o gráfico.
    :param titulo: Título do gráfico.
    :param xlabel: Nome da coluna do eixo X (deve ser categórica).
    :param ylabel: Nome da coluna do eixo Y (valores numéricos).
    :param nome_ficheiro: Nome base do arquivo de saída (opcional, padrão: "grafico").
    """
    try:
        logger.info(f"Iniciando a geração do gráfico de barras: {titulo}")

        # Verificar se df é um DataFrame
        if not isinstance(df, pd.DataFrame):
            raise ValueError("O parâmetro 'df' deve ser um pandas DataFrame.")

        # Verificar se as colunas existem
        if xlabel not in df.columns or ylabel not in df.columns:
            logger.warning(f"Erro: Colunas {xlabel} ou {ylabel} não encontradas no DataFrame.")
            logger.warning(f"Colunas disponíveis: {df.columns.tolist()}")
            return  

        # Criar diretório para armazenar gráficos
        caminho_projeto = os.path.dirname(os.path.abspath(__file__))
        caminho_data = os.path.join(caminho_projeto, "..", "graficos")
        os.makedirs(caminho_data, exist_ok=True)

        # Criar nome único para o arquivo
        data_atual = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        nome_completo = os.path.join(caminho_data, f"{nome_ficheiro}_{data_atual}.png")

        # Criar gráfico de barras
        plt.close('all')
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df, x=xlabel, y=ylabel, palette="Blues_r", ax=ax)

        # Configurações do gráfico
        plt.title(titulo, pad=20, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.xticks(rotation=45, ha='right')  
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Ajuste de layout
        plt.tight_layout()
        plt.savefig(nome_completo, dpi=300, bbox_inches="tight")
        logger.info(f"Gráfico salvo em: {nome_completo}")
        plt.close(fig)

    except Exception as e:
        logger.error(f"Erro ao gerar o gráfico de barras: {e}")

def gerar_grafico_linha(df, titulo, xlabel, ylabel, nome_ficheiro="grafico", hue=None):
    """
    Gera um gráfico de linha usando Seaborn e salva a imagem gerada.

    :param df: DataFrame contendo os dados para o gráfico.
    :param titulo: Título do gráfico.
    :param xlabel: Nome da coluna do eixo X (deve ser uma data no formato 'YYYY-MM').
    :param ylabel: Nome da coluna do eixo Y (valores numéricos).
    :param nome_ficheiro: Nome base do arquivo de saída (opcional, padrão: "grafico").
    :param hue: Nome da coluna categórica para colorir as linhas (exemplo: "Atendente").
    """
    try:
        logger.info(f"Iniciando a geração do gráfico de linha: {titulo}")

        # Verificar se df é um DataFrame
        if not isinstance(df, pd.DataFrame):
            raise ValueError("O parâmetro 'df' deve ser um pandas DataFrame.")

        # Verificar se as colunas existem
        if xlabel not in df.columns or ylabel not in df.columns:
            logger.warning(f"Erro: Colunas {xlabel} ou {ylabel} não encontradas no DataFrame.")
            logger.warning(f"Colunas disponíveis: {df.columns.tolist()}")
            return  

        # Criar diretório para armazenar gráficos
        caminho_projeto = os.path.dirname(os.path.abspath(__file__))
        caminho_data = os.path.join(caminho_projeto, "..", "graficos")
        os.makedirs(caminho_data, exist_ok=True)

        # Criar nome único para o arquivo
        data_atual = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        nome_completo = os.path.join(caminho_data, f"{nome_ficheiro}_{data_atual}.png")

        # Converter xlabel para datetime se for string
        if df[xlabel].dtype == "O":
            try:
                df[xlabel] = pd.to_datetime(df[xlabel], format="%Y-%m", errors="coerce")
            except Exception as e:
                logger.error(f"Erro ao converter '{xlabel}' para datetime: {e}")
                return  

        # Criar gráfico de linha
        plt.close('all')
        fig, ax = plt.subplots(figsize=(12, 6))

        if hue:
            sns.lineplot(data=df, x=xlabel, y=ylabel, hue=hue, marker="o", linestyle="-", ax=ax)
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title=hue)
        else:
            sns.lineplot(data=df, x=xlabel, y=ylabel, marker="o", linestyle="-", ax=ax)

        # Configurações do gráfico
        plt.title(titulo, pad=20, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.xticks(rotation=45, ha='right')  
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Ajuste de layout
        plt.tight_layout()
        plt.savefig(nome_completo, dpi=300, bbox_inches="tight")
        logger.info(f"Gráfico salvo em: {nome_completo}")
        plt.close(fig)

    except Exception as e:
        logger.error(f"Erro ao gerar o gráfico de linha: {e}")

import pandas as pd
import matplotlib.pyplot as plt
from utils.logger_utils import logging
from datetime import datetime
import os

def criar_graficos_matplotlib_pyplot(df, titulo, xlabel, ylabel, tipo="bar"):
    """
    Cria gráficos com base no DataFrame ou Series e nas opções fornecidas.

    :param df: DataFrame ou Series com os dados para o gráfico
    :param titulo: Título do gráfico
    :param xlabel: Rótulo do eixo X
    :param ylabel: Rótulo do eixo Y
    :param tipo: Tipo de gráfico (ex: "bar", "line")
    """
    if not isinstance(df, (pd.Series, pd.DataFrame)):
        raise ValueError("O parâmetro 'df' deve ser uma pandas Series ou DataFrame.")
    
    df.head(10).plot(kind=tipo, figsize=(10, 5))
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.show()


def guardar_analise_csv(df, nome_ficheiro):
    """
    Guarda um DataFrame ou Series como CSV dentro da pasta `data/`.

    :param df: DataFrame ou Series do Pandas com os dados a guardar.
    :param nome_ficheiro: Nome base do ficheiro CSV (sem extensão).
    """
    try:
        # Verifica se o df é um DataFrame ou Series válido
        if not isinstance(df, (pd.DataFrame, pd.Series)):
            raise ValueError("O parâmetro 'df' deve ser um pandas DataFrame ou Series.")

        # Obtém o caminho do diretório base do projeto
        caminho_projeto = os.path.dirname(os.path.abspath(__file__))  # Caminho do próprio ficheiro
        caminho_data = os.path.join(caminho_projeto, "..", "data")  # Garante que está dentro de 'data'

        # Criar a pasta "data" se não existir
        os.makedirs(caminho_data, exist_ok=True)

        # Adicionar a data ao nome do ficheiro
        data_atual = datetime.today().strftime('%Y-%m-%d')
        nome_completo = os.path.join(caminho_data, f"{nome_ficheiro}_{data_atual}.csv")

        # Se for uma Series, converte para DataFrame
        if isinstance(df, pd.Series):
            df = df.reset_index()

        # Guarda o ficheiro CSV
        df.to_csv(nome_completo, index=True)
        logging.info(f"Ficheiro guardado com sucesso: {nome_completo}")
    except Exception as e:
        logging.error(f"Erro ao tentar guardar o ficheiro: {e}")
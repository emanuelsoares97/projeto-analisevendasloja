import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime
from utils.logger_utils import get_logger

# Criar o logger para a função
logger = get_logger("GeradorGraficos")

def gerar_grafico(df, titulo, xlabel, ylabel, nome_ficheiro="grafico", tipo="bar"):
    """
    Gera um gráfico e salva a imagem com um nome único.
    
    :param df: DataFrame com os dados a serem representados.
    :param titulo: Título do gráfico.
    :param xlabel: Nome do eixo X.
    :param ylabel: Nome do eixo Y.
    :param nome_ficheiro: Nome base para o ficheiro de saída.
    :param tipo: Tipo de gráfico (ex: "bar", "line").
    """
    try:
        logger.info(f"Iniciando a geração do gráfico: {titulo}")

        # Validar se `df` é um DataFrame ou Series
        if not isinstance(df, (pd.DataFrame, pd.Series)):
            raise ValueError("O parâmetro 'df' deve ser um pandas DataFrame ou Series.")

        # Criar diretório para armazenar gráficos
        caminho_projeto = os.path.dirname(os.path.abspath(__file__))
        caminho_data = os.path.join(caminho_projeto, "..", "graficos")
        os.makedirs(caminho_data, exist_ok=True)

        # Criar nome único para o arquivo
        data_atual = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        nome_completo = os.path.join(caminho_data, f"{nome_ficheiro}_{data_atual}.png")

        # Fechar gráficos antigos para evitar sobreposição
        plt.close('all')
        fig, ax = plt.subplots(figsize=(14, 7))  # Ajustado para evitar cortes

        # Verificar se as colunas existem
        if xlabel in df.columns and ylabel in df.columns:
            df.plot(kind=tipo, x=xlabel, y=ylabel, ax=ax, legend=True)
            logger.info(f"Gráfico gerado com sucesso para {titulo}.")
        else:
            logger.warning(f"Erro: Colunas {xlabel} ou {ylabel} não encontradas no DataFrame.")
            logger.warning(f"Colunas disponíveis: {df.columns.tolist()}")
            return  # Sai da função se as colunas estiverem erradas

        #Configurações do gráfico
        plt.title(titulo, pad=20, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.xticks(rotation=45, ha='right')  # Melhor ajuste dos rótulos
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Ajuste de layout para evitar cortes
        plt.tight_layout()
        plt.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.25)

        # Formatar números no eixo Y
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(",", ".")))
        ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
        ax.yaxis.get_major_formatter().set_scientific(False)
        ax.yaxis.get_major_formatter().set_useOffset(False)

        # Guardar gráfico
        plt.savefig(nome_completo, dpi=300, bbox_inches="tight")
        logger.info(f"Gráfico salvo em: {nome_completo}")

        # Exibir gráfico
        plt.close(fig)

    except Exception as e:
        logger.error(f"Erro ao gerar o gráfico: {e}")

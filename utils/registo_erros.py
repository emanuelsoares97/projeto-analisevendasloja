import pandas as pd
from utils.logger_utils import get_logger
import os


logger_erros = get_logger("TratamentoErros")

def registrar_erros(df, coluna_verificacao, valor_invalido, nome_ficheiro):
    """
    Filtra registros inválidos e os salva em um log de erros.

    :param df: DataFrame contendo os dados.
    :param coluna_verificacao: Nome da coluna a verificar (ex: "Atendente").
    :param valor_invalido: Valor que indica erro (ex: "Desconhecido" ou NaN).
    :param nome_ficheiro: Nome base do arquivo de erro (ex: "erros_atendentes.csv").

    :return: DataFrame limpo, sem registros inválidos.
    """
    # Criar pasta logs se não existir
    caminho_logs = "logs"
    os.makedirs(caminho_logs, exist_ok=True)

    # Filtra registros inválidos
    if isinstance(valor_invalido, str):
        df_erros = df[df[coluna_verificacao] == valor_invalido]
    else:
        df_erros = df[df[coluna_verificacao].isna()]

    # Se houver erros, salvar no CSV de erros
    if not df_erros.empty:
        caminho_arquivo = os.path.join(caminho_logs, nome_ficheiro)
        df_erros.to_csv(caminho_arquivo, index=False)
        logger_erros.warning(f"{len(df_erros)} registros inválidos salvos em {caminho_arquivo}")

    # Retorna o DataFrame limpo, sem os registros inválidos
    return df.drop(df_erros.index)
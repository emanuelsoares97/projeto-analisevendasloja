import pandas as pd
import matplotlib.pyplot as plt
from utils.logger_utils import get_logger
from datetime import datetime
import matplotlib.ticker as ScalarFormatter
import os

def criar_graficos_matplotlib_pyplot(df, titulo, xlabel, ylabel, tipo="bar"):
    """
    USADO APENAS NO NOTEBOOK COMO BASE PARA A FUNCAO CRIADA EM GRAFICOS.PY

    Cria gráficos com base no DataFrame ou Series e nas opções fornecidas.

    :param df: DataFrame ou Series com os dados para o gráfico
    :param titulo: Título do gráfico
    :param xlabel: Rótulo do eixo X
    :param ylabel: Rótulo do eixo Y
    :param tipo: Tipo de gráfico (ex: "bar", "line")
    """
    if not isinstance(df, (pd.Series, pd.DataFrame)):
        raise ValueError("O parâmetro 'df' deve ser uma pandas Series ou DataFrame.")
    
    # Garante que o índice do gráfico seja a primeira coluna do DataFrame
    if isinstance(df, pd.DataFrame):
        df = df.set_index(df.columns[0])  # Define a primeira coluna como índice

    # Criar o gráfico
    ax = df.head(10).plot(kind=tipo, figsize=(10, 5))
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    # Configuração do eixo Y para evitar notação científica
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(False)  # Desativa notação científica
    ax.yaxis.get_major_formatter().set_useOffset(False)  # Remove deslocamento

    plt.legend(loc="upper right")  # Ajusta a posição da legenda
    plt.show()

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

loggercv= get_logger("guardar_analise_csv")
def guardar_analise_csv(df, nome_ficheiro):
    """
    Guarda um DataFrame ou Series como CSV dentro da pasta `data/analisescsv`, garantindo que os ficheiros não sejam sobrescritos.

    :param df: DataFrame ou Series do Pandas com os dados a guardar.
    :param nome_ficheiro: Nome base do ficheiro CSV (sem extensão).
    """
    try:
        if not isinstance(df, (pd.DataFrame, pd.Series)):
            loggercv.error(f"Erro ao tentar guardar o ficheiro: {ValueError}")
            raise ValueError("O parâmetro 'df' deve ser um pandas DataFrame ou Series.")
        
        # Obtém o caminho do diretório base do projeto
        caminho_projeto = os.path.dirname(os.path.abspath(__file__))
        caminho_data = os.path.join(caminho_projeto, "..", "data/analisescsv")

        # Criar a pasta "analisescsv" se não existir
        os.makedirs(caminho_data, exist_ok=True)

        # Adicionar a data e hora ao nome do ficheiro (formato YYYY-MM-DD_HH-MM-SS)
        data_atual = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        nome_completo = os.path.join(caminho_data, f"{nome_ficheiro}_{data_atual}.csv")

        # Se for uma Series, converte para DataFrame
        if isinstance(df, pd.Series):
            df = df.reset_index()

        # Guarda o ficheiro CSV
        df.to_csv(nome_completo, index=True)
        loggercv.info(f"Ficheiro guardado com sucesso: {nome_completo}")
    
    except Exception as e:
        loggercv.error(f"Erro ao tentar guardar o ficheiro: {e}")


loggermerge=get_logger("merge_tabelas")

def merge_tabelas(db_manager):
    """
    Junta as tabelas vendas, produtos, clientes, lojas e atendentes.
    :param db_manager: Instância do DatabaseManager para carregar os dados.
    :return: DataFrame final com todas as tabelas unidas.
    """

    # Carregar dados das tabelas
    df_vendas = db_manager.fetch_data_to_df("SELECT * FROM vendas;")
    df_produtos = db_manager.fetch_data_to_df("SELECT * FROM produtos;")
    df_clientes = db_manager.fetch_data_to_df("SELECT * FROM clientes;")
    df_lojas = db_manager.fetch_data_to_df("SELECT * FROM lojas;")
    df_atendentes = db_manager.fetch_data_to_df("SELECT * FROM atendentes;")

    loggermerge.info(f"Tabelas carregadas com sucesso.")
    loggermerge.info(f"Colunas disponíveis:\n"
                     f"Vendas: {df_vendas.columns}\n"
                     f"Produtos: {df_produtos.columns}\n"
                     f"Clientes: {df_clientes.columns}\n"
                     f"Lojas: {df_lojas.columns}\n"
                     f"Atendentes: {df_atendentes.columns}")

    # Garantir que as colunas necessárias existem antes do merge
    required_columns = {
        "vendas": ["ID_Venda", "ID_Produto", "ID_Cliente", "ID_Loja", "ID_Atendente", "Quantidade"],
        "produtos": ["ID_Produto", "Nome_Produto", "Categoria", "Preço"],
        "clientes": ["ID_Cliente", "Nome"],
        "lojas": ["ID_Loja", "Nome_Loja"],
        "atendentes": ["ID_Atendente", "Nome"]
    }

    for table_name, cols in required_columns.items():
        df = eval(f"df_{table_name}")  # Obtém dinamicamente o DataFrame correto
        missing_cols = [col for col in cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"A tabela '{table_name}' não contém as colunas necessárias: {missing_cols}")

    # Merge das tabelas
    df_merged = df_vendas.merge(df_produtos, on="ID_Produto", how="left")
    df_merged = df_merged.merge(df_clientes, on="ID_Cliente", how="left")
    df_merged = df_merged.merge(df_lojas, on="ID_Loja", how="left")
    df_merged = df_merged.merge(df_atendentes, on="ID_Atendente", how="left")

    loggermerge.info("Merge das tabelas realizado com sucesso.")

    # **Garantir que 'Preço' e 'Quantidade' existem antes de criar 'Receita Total'**
    if "Preço" in df_merged.columns and "Quantidade" in df_merged.columns:
        df_merged["Receita Total"] = df_merged["Preço"] * df_merged["Quantidade"]
        loggermerge.info("Coluna 'Receita Total' criada.")
    else:
        raise ValueError("Erro ao criar 'Receita Total': Colunas 'Preço' ou 'Quantidade' não encontradas.")

    # Renomear colunas para manter consistência
    df_merged.rename(columns={
        "ID_Venda": "ID Venda",
        "ID_Produto": "ID Produto",
        "ID_Cliente": "ID Cliente",
        "ID_Loja": "ID Loja",
        "ID_Atendente": "ID Atendente",
        "Nome_Produto": "Produto",
        "Preço": "Preco",  # Padronizar nome sem acento
        "Quantidade": "Quantidade",
        "Nome_Loja": "Loja",
        "Nome_x": "Cliente",  # Nome correto do cliente
        "Nome_y": "Atendente"  # Nome correto do atendente
    }, inplace=True)

    # Tratar valores nulos
    df_merged.fillna({
        "Quantidade": 0,  # Se não tiver quantidade, assume 0
        "Receita_Total": 0,  # Se faltar preço ou quantidade, assume 0
        "Atendente": "Desconhecido",  # Se não tiver atendente, preenche com "Desconhecido"
        "Loja": "Não Informado",  # Se não tiver loja, coloca "Não Informado"
        "Produto": "Desconhecido",  # Produto sem nome recebe "Desconhecido"
    }, inplace=True)

    loggermerge.info(f"Colunas renomeadas: {df_merged.columns}")

    return df_merged


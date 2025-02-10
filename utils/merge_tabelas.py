from utils.registo_erros import registrar_erros
import pandas as pd
from utils.logger_utils import get_logger

loggermerge = get_logger("merge_tabelas")

def merge_tabelas(db_manager, formatar_data=True):
    """
    Junta as tabelas vendas, produtos, clientes, lojas e atendentes.
    
    :param db_manager: Instância do DatabaseManager para carregar os dados.
    :param formatar_data: Se True, formata a data para "YYYY-MM".
    :return: DataFrame final com todas as tabelas unidas.
    """

    # Carregar dados das tabelas
    df_vendas = db_manager.fetch_data_to_df("SELECT * FROM vendas;")
    df_produtos = db_manager.fetch_data_to_df("SELECT * FROM produtos;")
    df_clientes = db_manager.fetch_data_to_df("SELECT * FROM clientes;")
    df_lojas = db_manager.fetch_data_to_df("SELECT * FROM lojas;")
    df_atendentes = db_manager.fetch_data_to_df("SELECT * FROM atendentes;")

    loggermerge.info("Tabelas carregadas com sucesso.")

    # Criar um dicionário de tabelas
    tabelas = {
        "vendas": df_vendas,
        "produtos": df_produtos,
        "clientes": df_clientes,
        "lojas": df_lojas,
        "atendentes": df_atendentes
    }

    # Garantir que todas as colunas necessárias estão presentes
    required_columns = {
        "vendas": ["ID_Venda", "ID_Produto", "ID_Cliente", "ID_Loja", "ID_Atendente", "Quantidade"],
        "produtos": ["ID_Produto", "Nome_Produto", "Categoria", "Preço"],
        "clientes": ["ID_Cliente", "Nome"],
        "lojas": ["ID_Loja", "Nome_Loja"],
        "atendentes": ["ID_Atendente", "Nome"]
    }

    for table_name, cols in required_columns.items():
        df = tabelas[table_name]
        missing_cols = [col for col in cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"A tabela '{table_name}' não contém as colunas necessárias: {missing_cols}")

    # Merge das tabelas
    df_merged = df_vendas.merge(df_produtos, on="ID_Produto", how="left")
    df_merged = df_merged.merge(df_clientes, on="ID_Cliente", how="left")
    df_merged = df_merged.merge(df_lojas, on="ID_Loja", how="left")
    df_merged = df_merged.merge(df_atendentes, on="ID_Atendente", how="left")

    loggermerge.info("Merge das tabelas realizado com sucesso.")

    # Criar Receita Total
    if "Preço" in df_merged.columns and "Quantidade" in df_merged.columns:
        df_merged["Receita Total"] = df_merged["Preço"] * df_merged["Quantidade"]
    else:
        loggermerge.error("Erro ao criar 'Receita Total': Colunas 'Preço' ou 'Quantidade' não encontradas.")
        raise ValueError("Erro ao criar 'Receita Total': Colunas 'Preço' ou 'Quantidade' não encontradas.")

    # Renomear colunas para manter consistência
    df_merged.rename(columns={
        "ID_Venda": "ID Venda",
        "ID_Produto": "ID Produto",
        "ID_Cliente": "ID Cliente",
        "ID_Loja": "ID Loja",
        "ID_Atendente": "ID Atendente",
        "Nome_Produto": "Produto",
        "Preço": "Preco",
        "Quantidade": "Quantidade",
        "Nome_Loja": "Loja",
        "Nome_x": "Cliente",
        "Nome_y": "Atendente"
    }, inplace=True)

    # Registrar erros antes do tratamento de nulos
    df_merged = registrar_erros(df_merged, "Atendente", "Desconhecido", "erros_atendentes.csv")
    df_merged = registrar_erros(df_merged, "Receita Total", None, "erros_receita.csv")

    # Tratar valores nulos
    valores_nulos = {
        "Quantidade": 0,
        "Receita Total": 0,
        "Atendente": "Desconhecido",
        "Loja": "Não Informado",
        "Produto": "Desconhecido"
    }
    df_merged.fillna(valores_nulos, inplace=True)

    # Garantir que a coluna "Data" está no formato datetime
    df_merged["Data"] = pd.to_datetime(df_merged["Data"], errors='coerce')

    # Remover valores nulos na coluna Data
    df_merged = df_merged[df_merged["Data"].notna()]

    # Obter o ano mais recente disponível nos dados
    ano_mais_recente = df_merged["Data"].dt.year.max()

    # Filtrar apenas para o ano mais recente
    df_merged = df_merged[df_merged["Data"].dt.year == ano_mais_recente]

    # Formatar data, se necessário
    if formatar_data:
        df_merged["Ano_Mes"] = df_merged["Data"].dt.strftime("%Y-%m")

    loggermerge.info(f"Colunas renomeadas: {df_merged.columns}")

    return df_merged

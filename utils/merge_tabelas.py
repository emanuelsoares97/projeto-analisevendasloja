from utils.funcoes import get_logger
from utils.registo_erros import registrar_erros
import pandas as pd
from utils.logger_utils import get_logger


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

    # Garantir que 'Preço' e 'Quantidade' existem antes de criar 'Receita Total'
    if "Preço" in df_merged.columns and "Quantidade" in df_merged.columns:
        df_merged["Receita Total"] = df_merged["Preço"] * df_merged["Quantidade"]
        loggermerge.info("Coluna 'Receita Total' criada.")
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
        "Preço": "Preco",  # Padronizar nome sem acento
        "Quantidade": "Quantidade",
        "Nome_Loja": "Loja",
        "Nome_x": "Cliente",  # Nome correto do cliente
        "Nome_y": "Atendente"  # Nome correto do atendente
    }, inplace=True)

    # **Registrar erros antes do tratamento de nulos**
    df_merged = registrar_erros(df_merged, "Atendente", "Desconhecido", "erros_atendentes.csv")
    df_merged = registrar_erros(df_merged, "Receita Total", None, "erros_receita.csv")

    # Tratar valores nulos (depois de mover erros)
    df_merged.fillna({
        "Quantidade": 0,  # Se não tiver quantidade, assume 0
        "Receita Total": 0,  # Se faltar preço ou quantidade, assume 0
        "Atendente": "Desconhecido",  # Se não tiver atendente, preenche com "Desconhecido"
        "Loja": "Não Informado",  # Se não tiver loja, coloca "Não Informado"
        "Produto": "Desconhecido",  # Produto sem nome recebe "Desconhecido"
    }, inplace=True)

    loggermerge.info(f"Colunas renomeadas: {df_merged.columns}")

    return df_merged
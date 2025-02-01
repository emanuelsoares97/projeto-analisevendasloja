import os
import sqlite3
import pandas as pd
from classes.classdatabasemanager import DatabaseManager
from utils.logger_utils import logging

def apagar_base_dados():
    """Apaga a base de dados SQLite se existir."""
    caminho_db = "database/loja.db"
    if os.path.exists(caminho_db):
        os.remove(caminho_db)
        logging.info("🗑️ Base de dados apagada: loja.db")
    else:
        logging.info("ℹ️ Nenhuma base de dados encontrada para apagar.")

def criar_base_dados():
    """Cria a estrutura do banco de dados e suas tabelas."""
    db_manager = DatabaseManager()
    db_manager.create_table()
    logging.info("✅ Estrutura do banco de dados recriada com sucesso.")

def carregar_dados():
    """Carrega os dados dos CSVs para a base de dados."""
    db_manager = DatabaseManager()
    
    arquivos_csv = {
        "lojas": "data/Lojas.csv",
        "atendentes": "data/Atendentes.csv",
        "produtos": "data/Produtos.csv",
        "clientes": "data/Clientes.csv",
        "vendas": "data/Vendas.csv"
    }

    for tabela, caminho in arquivos_csv.items():
        if os.path.exists(caminho):
            db_manager.load_csv_to_table(caminho, tabela)
            logging.info(f"📂 Dados carregados para a tabela '{tabela}'.")
        else:
            logging.warning(f"⚠️ Arquivo CSV não encontrado: {caminho}")

def verificar_dados():
    """Verifica se os dados foram carregados corretamente."""
    db_manager = DatabaseManager()
    
    tabelas = ["lojas", "atendentes", "produtos", "clientes", "vendas"]
    
    for tabela in tabelas:
        df = db_manager.fetch_data_to_df(f"SELECT * FROM {tabela} LIMIT 5;")
        logging.info(f"🔹 {tabela.capitalize()} (Primeiros 5 registros):")
        print(df)

def reset_sistema():
    """Executa todo o processo de reset."""
    logging.info("🔄 Iniciando o reset da base de dados...")
    apagar_base_dados()
    criar_base_dados()
    carregar_dados()
    verificar_dados()
    logging.info("🚀 Reset concluído com sucesso!")

if __name__ == "__main__":
    reset_sistema()

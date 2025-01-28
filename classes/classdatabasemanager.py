import sqlite3
import pandas as pd
import logging

class DatabaseManager:
    def __init__(self, db_path):
        """Inicializa a classe com o caminho do banco de dados."""
        self.db_path = db_path

    def execute_query(self, query, params=None):
        """
        Executa uma query SQL no banco de dados.
        - query: Comando SQL (string).
        - params: Parâmetros para a query (tuple ou list).
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON;")  # Ativar FOREIGN KEYS aqui
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
                logging.info(f"Query executada com sucesso: {query}")
        except sqlite3.Error as e:
            logging.error(f"Erro ao executar a query: {e}")
            raise



    def fetch_data(self, query, params=None):
        """
        Executa uma query SQL e retorna os dados.
        - query: Comando SQL (string).
        - params: Parâmetros para a query (tuple ou list).
        - Retorna: Lista de tuplas com os resultados.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()


    def fetch_data_to_df(self, query, params=None):
        """
        Executa uma query SQL e retorna os dados em um DataFrame.
        - query: Comando SQL (string).
        - params: Parâmetros para a query (tuple ou list).
        - Retorna: DataFrame com os resultados.
        """
        with sqlite3.connect(self.db_path) as conn:
            if params:
                return pd.read_sql_query(query, conn, params=params)
            return pd.read_sql_query(query, conn)

    def save_df_to_table(self, df, table_name):
        """
        Salva um DataFrame no banco de dados.
        - df: DataFrame a ser salvo.
        - table_name: Nome da tabela no banco de dados.
        """
        with sqlite3.connect(self.db_path) as conn:
            df.to_sql(table_name, conn, if_exists="replace", index=False)

    def create_table(self):
        """
        Cria as tabelas necessárias no banco de dados.
        """
        tabela_produtos="""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    preco INTEGER NOT NULL
);
"""
        tabela_clientes="""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL
);
"""
        tabela_vendas="""
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY,
    id_produto INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    data DATE NOT NULL,
    FOREIGN KEY (id_produto) REFERENCES produtos (id),
    FOREIGN KEY (id_cliente) REFERENCES clientes (id)
);

"""
 
        self.execute_query(tabela_produtos)
        self.execute_query(tabela_vendas)
        self.execute_query(tabela_clientes)

    def execute_many(self, query, params_list):
        """
        Executa uma query SQL para múltiplos registros.
        :param query: Comando SQL.
        :param params_list: Lista de tuplas com os parâmetros.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()


    def load_csv_to_table(self, file_path, table_name):
        """
        Carrega os dados de um arquivo CSV para uma tabela no banco de dados.
        :param file_path: Caminho para o arquivo CSV.
        :param table_name: Nome da tabela no banco de dados.
        """
        try:
            # Ler o CSV usando pandas
            df = pd.read_csv(file_path)
            # Salvar os dados na tabela SQLite
            with sqlite3.connect(self.db_path) as conn:
                df.to_sql(table_name, conn, if_exists="append", index=False)
            print(f"Dados do arquivo {file_path} carregados na tabela '{table_name}' com sucesso.")
        except Exception as e:
            print(f"Erro ao carregar {file_path} na tabela '{table_name}': {e}")

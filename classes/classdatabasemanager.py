import sqlite3
import pandas as pd
from utils.logger_utils import get_logger
import os


class DatabaseManager:
    def __init__(self, db_path=None):
        """Inicializa a classe com o caminho do banco de dados."""
        self.logger=get_logger("DatabaseManager")
        if db_path is None:
            # Obtém automaticamente o caminho absoluto da raiz do projeto
            root_dir = os.path.dirname(os.path.abspath(__file__))  # Caminho do arquivo atual
            root_dir = os.path.dirname(root_dir)  # Sobe um nível para a raiz do projeto
            db_path = os.path.join(root_dir, "database", "loja.db")

        self.db_path = db_path
        self.logger.info(f"Usando banco de dados: {self.db_path}")

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
                self.logger.info(f"Query executada com sucesso: {query}")
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao executar a query: {e}")
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco INTEGER NOT NULL,
    categoria TEXT NOT NULL
);
"""
        tabela_clientes="""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    id_loja INTEGER NOT NULL,
    FOREIGN KEY (id_loja) REFERENCES lojas(id_loja)
);
"""
        tabela_vendas="""
CREATE TABLE IF NOT EXISTS vendas (
    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
    id_produto INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_loja INTEGER NOT NULL,
    id_atendente INTEGER NOT NULL,  -- NOVO CAMPO
    quantidade INTEGER NOT NULL,
    data DATE NOT NULL,
    FOREIGN KEY (id_produto) REFERENCES produtos(id),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    FOREIGN KEY (id_loja) REFERENCES lojas(id),
    FOREIGN KEY (id_atendente) REFERENCES atendentes(id_atendente) -- RELACIONANDO A VENDA COM O ATENDENTE
);
"""
        tabela_lojas="""
CREATE TABLE IF NOT EXISTS lojas (
    id_loja INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_loja TEXT NOT NULL,
    zona_loja TEXT NOT NULL,
    gerente TEXT NOT NULL
);
"""
        tabela_atendentes="""CREATE TABLE IF NOT EXISTS atendentes (
    id_atendente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_atendente TEXT NOT NULL,
    id_loja INTEGER NOT NULL,
    FOREIGN KEY (id_loja) REFERENCES lojas(id_loja)
);
"""

        # Criar tabelas na ordem correta
        self.execute_query(tabela_lojas)
        self.logger.info("Criada a tabela lojas.")

        self.execute_query(tabela_atendentes)
        self.logger.info("Criada a tabela atendentes.")

        self.execute_query(tabela_clientes)
        self.logger.info("Criada a tabela clientes.")

        self.execute_query(tabela_produtos)
        self.logger.info("Criada a tabela produtos.")

        self.execute_query(tabela_vendas)
        self.logger.info("Criada a tabela vendas.")

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
                df.to_sql(table_name, conn, if_exists="replace", index=False)
            self.logger.info(f"Dados do arquivo {file_path} carregados na tabela '{table_name}' com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao carregar {file_path} na tabela '{table_name}': {e}")

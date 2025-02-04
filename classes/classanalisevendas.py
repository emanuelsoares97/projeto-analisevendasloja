import pandas as pd
from utils.funcoes import guardar_analise_csv
from utils.merge_tabelas import merge_tabelas
from utils.logger_utils import get_logger
from datetime import datetime

class AnaliseVendas:
    def __init__(self, db_manager):
        """Inicializa a classe carregando os dados do banco."""
        self.logger = get_logger("AnaliseVendas")
        self.db_manager = db_manager
        self.df_merged = merge_tabelas(db_manager)
        self.logger.info(f"Colunas após o merge: {self.df_merged.columns}")

        self.logger.info("Base de dados carregada e normalizada para análises.")

    def calcular_receita_por_produto(self):
        """Calcula a receita total por produto e guarda num CSV."""
        try:
            self.df_merged["Receita Total"] = self.df_merged["Preco"] * self.df_merged["Quantidade"]
            receita_por_produto = self.df_merged.groupby("Produto")["Receita Total"].sum().sort_values(ascending=False).reset_index()

            # Guardar CSV
            guardar_analise_csv(receita_por_produto, "top10_receita_por_produto")
            self.logger.info("Ficheiro guardado: top10_receita_por_produto")

            return receita_por_produto

        except Exception as e:
            self.logger.error(f"Erro ao calcular receita por produto: {e}")
            return None

    def calcular_produtos_mais_vendidos(self):
        """Calcula os produtos mais vendidos (quantidade total)."""
        try:
            produtos_vendidos = self.df_merged.groupby("Produto")["Quantidade"].sum().sort_values(ascending=False).reset_index()

            # Guardar CSV
            guardar_analise_csv(produtos_vendidos, "top10_produtos_mais_vendidos")
            self.logger.info("Ficheiro guardado: top10_produtos_mais_vendidos")

            return produtos_vendidos

        except Exception as e:
            self.logger.error(f"Erro ao calcular produtos mais vendidos: {e}")
            return None
        
    def calcular_total_vendas_mes(self):
        """Calcular o total de receita por mês para o ano mais recente disponível"""
        try:
            # Converter a coluna "Data" para datetime, tratando possíveis erros
            self.df_merged["Data"] = pd.to_datetime(self.df_merged["Data"], errors='coerce')

            # Remover valores nulos na Data
            self.df_merged.dropna(subset=["Data"], inplace=True)

            # Obter o ano mais recente presente nos dados
            ano_mais_recente = self.df_merged["Data"].dt.year.max()
            self.logger.info(f"Ano mais recente detectado: {ano_mais_recente}")

            # Filtrar apenas os dados do ano mais recente
            df_filtrado = self.df_merged[self.df_merged["Data"].dt.year == ano_mais_recente]

            # Agrupar por mês e somar a receita total
            df_vendas_tempo = df_filtrado.groupby(pd.Grouper(key="Data", freq="ME"))["Receita Total"].sum().reset_index()

            # Formatar a data como "YYYY-MM" para facilitar a visualização
            df_vendas_tempo["Data"] = df_vendas_tempo["Data"].dt.strftime("%Y-%m")

            # Ordenar os meses em ordem crescente
            df_vendas_tempo = df_vendas_tempo.sort_values("Data", ascending=True)

            self.logger.info(f"Vendas calculadas para o ano {ano_mais_recente}:\n{df_vendas_tempo}")

            return df_vendas_tempo

        except Exception as e:
            self.logger.error(f"Erro ao calcular vendas por mês: {e}")
            raise Exception(f"Erro ao calcular vendas por mês: {e}")
            
    def calcular_total_vendas_ano(self):
        try:
            self.df_merged["Data"] = pd.to_datetime(self.df_merged["Data"])
            df_vendas_tempo = self.df_merged.groupby(pd.Grouper(key="Data", freq="Y"))["Receita Total"].sum().reset_index()
            df_vendas_tempo["Data"] = df_vendas_tempo["Data"].dt.strftime("%Y")
            df_vendas_tempo = df_vendas_tempo.sort_values("Data", ascending=False)
        except Exception as e:
            self.logger.info(f"Erro ao tentar validar vendas por ano, erro: {e}")
            raise (f"Erro ao tentar validar vendas por data, erro: {e}")
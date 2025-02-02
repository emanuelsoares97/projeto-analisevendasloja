import pandas
from utils.funcoes import guardar_analise_csv, merge_tabelas
from utils.logger_utils import get_logger

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
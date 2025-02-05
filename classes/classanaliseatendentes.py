import pandas as pd
from utils.funcoes import guardar_analise_csv
from utils.merge_tabelas import merge_tabelas
from utils.logger_utils import get_logger
from datetime import datetime

class AnaliseAtendentes:
    def __init__(self, db_manager):
        """Inicializa a classe carregando os dados do banco."""
        self.logger = get_logger("AnaliseAtendentes")
        self.db_manager = db_manager

        try:
            self.df_merged = merge_tabelas(db_manager)

            # Garantir que as colunas necessárias estão no DataFrame
            required_columns = ["Atendente", "ID Atendente", "Quantidade", "Receita Total", "Loja", "Data"]
            missing_cols = [col for col in required_columns if col not in self.df_merged.columns]

            if missing_cols:
                raise ValueError(f"Colunas ausentes no DataFrame após merge: {missing_cols}")

            self.df_merged = self.df_merged[required_columns]
            self.logger.info(f"Colunas após o merge: {self.df_merged.columns}")
            self.logger.info("Base de dados carregada e normalizada para análises.")

        except Exception as e:
            self.logger.error(f"Erro ao carregar os dados do banco: {e}")
            self.df_merged = None  # Garante que não será usado se falhar

    def atendentes_mais_venderam(self):
        """Calcula a quantidade total de produtos vendidos por atendente e guarda em CSV."""
        try:
            if self.df_merged is None:
                raise ValueError("Os dados não foram carregados corretamente.")

            atendentes_mais_vendas = self.df_merged.groupby("Atendente")["Quantidade"].sum().sort_values(ascending=False).reset_index()

            # Guardar CSV
            guardar_analise_csv(atendentes_mais_vendas, "top10_atendentes_vendas")
            self.logger.info("Ficheiro guardado: top10_atendentes_vendas")

            return atendentes_mais_vendas.head(10)

        except Exception as e:
            self.logger.error(f"Erro ao calcular atendentes que mais venderam: {e}")
            return None

    def atendentes_mais_faturaram(self):
        """Calcula o total de faturamento por atendente e guarda em CSV."""
        try:
            if self.df_merged is None:
                raise ValueError("Os dados não foram carregados corretamente.")

            atendentes_mais_receita = self.df_merged.groupby("Atendente")["Receita Total"].sum().sort_values(ascending=False).reset_index()

            # Guardar CSV
            guardar_analise_csv(atendentes_mais_receita, "top10_atendentes_receita")
            self.logger.info("Ficheiro guardado: top10_atendentes_receita")

            return atendentes_mais_receita.head(10)

        except Exception as e:
            self.logger.error(f"Erro ao calcular atendentes que mais faturaram: {e}")
            return None

    def atendentes_ticket_medio_venda(self):
        """Calcula o ticket médio por atendente e guarda em CSV."""
        try:
            if self.df_merged is None:
                raise ValueError("Os dados não foram carregados corretamente.")

            df_ticket_medio = self.df_merged.groupby("Atendente").agg({"Receita Total": "sum", "Quantidade": "sum"})
            df_ticket_medio["Ticket Médio"] = round(df_ticket_medio["Receita Total"] / df_ticket_medio["Quantidade"], 2)
            df_ticket_medio = df_ticket_medio.sort_values(by="Ticket Médio", ascending=False).reset_index()

            # Guardar CSV
            guardar_analise_csv(df_ticket_medio, "top10_ticket_medio")
            self.logger.info("Ficheiro guardado: top10_ticket_medio")

            return df_ticket_medio.head(10)

        except Exception as e:
            self.logger.error(f"Erro ao calcular ticket médio dos atendentes: {e}")
            return None

    def evolucao_vendas_por_atendente(self):
        """
        Calcula a evolução do faturamento ao longo do tempo para cada atendente.
        :return: DataFrame com evolução das vendas ao longo do tempo.
        """
        try:
            # Garantir que a coluna "Data" está no formato datetime
            self.df_merged["Data"] = pd.to_datetime(self.df_merged["Data"], errors='coerce')

            # Remover valores nulos após conversão
            self.df_merged = self.df_merged.dropna(subset=["Data"])

            # Obter o ano mais recente disponível nos dados
            ano_mais_recente = self.df_merged["Data"].dt.year.max()

            # Filtrar apenas para o ano mais recente
            df_filtrado = self.df_merged[self.df_merged["Data"].dt.year == ano_mais_recente]

            # Agrupar por Data e Atendente para calcular o faturamento
            df_vendas_tempo = df_filtrado.groupby(["Data", "Atendente"])["Receita Total"].sum().reset_index()

            #formato ano e mes
            df_vendas_tempo["Data"] = pd.to_datetime(df_vendas_tempo["Data"]).dt.strftime("%Y-%m")

            # Ordenar os meses em ordem crescente
            df_vendas_tempo = df_vendas_tempo.sort_values("Data", ascending=True)

            self.logger.info("Evolução de vendas por atendente calculada com sucesso.")
            return df_vendas_tempo

        except Exception as e:
            self.logger.error(f"Erro ao calcular evolução de vendas por atendente: {e}")
            return None
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from utils.funcoes import guardar_analise_csv
from utils.merge_tabelas import merge_tabelas
from utils.logger_utils import get_logger
from datetime import datetime

class AnaliseLojas:
    def __init__(self, db_manager):
        """Inicializa a classe carregando os dados do banco."""
        self.logger = get_logger("AnaliseLojas")
        self.db_manager = db_manager
        self.df_merged = merge_tabelas(db_manager)

    def total_faturado_por_loja(self):
        """Calcula o total faturado por loja."""
        faturado_loja = self.df_merged.groupby("Loja")["Receita Total"].sum().sort_values(ascending=False).reset_index()
        guardar_analise_csv(faturado_loja, "total_faturado_loja")
        self.logger.info("Tabela guardada: total faturado por loja.")
        return faturado_loja.head(10)

    def total_vendas_por_loja(self):
        """Calcula a quantidade total de vendas por loja."""
        vendas_loja = self.df_merged.groupby("Loja")["Quantidade"].sum().sort_values(ascending=False).reset_index()
        guardar_analise_csv(vendas_loja, "total_vendas_por_loja")
        self.logger.info("Tabela guardada: total de vendas por loja.")
        return vendas_loja.head(10)

    def media_ticket_loja(self):
        """Calcula o ticket médio por loja."""
        media_ticket = self.df_merged.groupby("Loja").agg({"Receita Total": "sum", "Quantidade": "sum"}).reset_index()
        media_ticket["Ticket Médio"] = round(media_ticket["Receita Total"] / media_ticket["Quantidade"], 2)
        media_ticket = media_ticket.sort_values(by="Ticket Médio", ascending=False)[["Loja", "Ticket Médio"]]
        guardar_analise_csv(media_ticket, "media_ticket_loja")
        self.logger.info("Tabela guardada: ticket médio por loja.")
        return media_ticket.head(10)

    def atendentes_por_loja(self):
        """Tabela com o número de atendentes por loja."""
        try:
            if self.df_merged is None:
                raise ValueError("Os dados não foram carregados corretamente.")

            atendentes_por_loja = self.df_merged.groupby("Loja")["Atendente"].nunique().reset_index()
            atendentes_por_loja.rename(columns={"Atendente": "Número de Atendentes"}, inplace=True)

            # Guardar CSV
            guardar_analise_csv(atendentes_por_loja, "atendentes_por_loja")
            self.logger.info("Ficheiro guardado: atendentes_por_loja")

            return atendentes_por_loja

        except Exception as e:
            self.logger.error(f"Erro ao calcular número de atendentes por loja: {e}")
            return None


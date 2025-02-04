import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from utils.funcoes import guardar_analise_csv
from utils.merge_tabelas import merge_tabelas
from utils.logger_utils import get_logger
from datetime import datetime

class AnaliseClientes:
    def __init__(self, db_manager):
        """Inicializa a classe carregando os dados do banco."""
        self.logger = get_logger("AnaliseClientes")
        self.db_manager = db_manager
        self.df_merged = merge_tabelas(db_manager)

    def calcular_total_gasto_por_cliente(self):
        """Calcula o total gasto por cliente."""
        
        cliente_gasto = self.df_merged.groupby("Cliente")["Receita Total"].sum().sort_values(ascending=False).reset_index()
        guardar_analise_csv(cliente_gasto, "top10_total_gasto_cliente")
        self.logger.info("Tabela guardada: total gasto por cliente.")
        return cliente_gasto.head(10)

    def calcular_total_compras_por_cliente(self):
        """Calcula a quantidade total de produtos comprados por cliente."""
        cliente_compras = self.df_merged.groupby("Cliente")["Quantidade"].sum().sort_values(ascending=False).reset_index()
        guardar_analise_csv(cliente_compras, "top10_total_compras_cliente")
        self.logger.info("Tabela guardada: total compras por cliente.")
        return cliente_compras.head(10)


import pandas as pd
from utils.merge_tabelas import merge_tabelas
from utils.logger_utils import get_logger
from classes.classanaliselojas import AnaliseLojas 
from classes.classanaliseatendentes import AnaliseAtendentes
from classes.classanalisevendas import AnaliseVendas
from utils.graficos import gerar_grafico

# Configurar logger
logger = get_logger("Relatorio Vendas")

def gerar_relatorio_vendas(db_manager):
    """
    Gera um relatório final com os principais indicadores de vendas.
    """
    logger.info("Iniciar relatorio vendas final.")

    # Criar instância da classe de análise
    analise_vendas = AnaliseVendas(db_manager)

    #receita total por produto
    receita_df = analise_vendas.calcular_receita_por_produto()
    gerar_grafico(receita_df, "Top 10 Produtos com Maior Receita", "Produto", "Receita Total", "top10_receita")
    produtos_vendidos_df = analise_vendas.calcular_produtos_mais_vendidos()
    gerar_grafico(produtos_vendidos_df, "Top 10 Produtos Mais Vendidos", "Produto", "Quantidade", "top10_vendas")
    

    logger.info("Relatório gerado com sucesso.")

if __name__ == "__main__":
    from classes.classdatabasemanager import DatabaseManager
    db_manager = DatabaseManager()
    gerar_relatorio(db_manager)

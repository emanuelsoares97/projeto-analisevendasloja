from classes.classdatabasemanager import DatabaseManager
from classes.classanalisevendas import AnaliseVendas
from classes.classanaliseclientes import AnaliseClientes
from classes.classanaliselojas import AnaliseLojas
from utils.logger_utils import get_logger
from utils.graficos import gerar_grafico

# Criar o logger para a main
logger = get_logger("Main")

def main():
    try:
        db_manager = DatabaseManager()
        
        # Criar instâncias das análises
        analise_vendas = AnaliseVendas(db_manager)
        analise_clientes = AnaliseClientes(db_manager)
        analise_lojas = AnaliseLojas(db_manager)

        # Executar todas as análises
        logger.info("Gerar análises de vendas...")
        receita_df = analise_vendas.calcular_receita_por_produto()
        gerar_grafico(receita_df, "Top 10 Produtos com Maior Receita", "Produto", "Receita Total", "top10_receita")
        produtos_vendidos_df = analise_vendas.calcular_produtos_mais_vendidos()
        gerar_grafico(produtos_vendidos_df, "Top 10 Produtos Mais Vendidos", "Produto", "Quantidade", "top10_vendas")

        logger.info("Gerar análises de clientes...")
        clientes_gasto_df = analise_clientes.calcular_total_gasto_por_cliente()
        gerar_grafico(clientes_gasto_df, "Top 10 Clientes que Mais Gastaram", "Cliente", "Receita Total", "top10_gasto_clientes")
        clientes_qtd_df = analise_clientes.calcular_total_compras_por_cliente()
        gerar_grafico(clientes_qtd_df, "Top 10 Clientes que Mais Compraram", "Cliente", "Quantidade", "top10_qtd_clientes")

        logger.info("Gerar análises de lojas...")
        faturado_loja_df = analise_lojas.total_faturado_por_loja()
        gerar_grafico(faturado_loja_df, "Total Faturado por Loja", "Loja", "Receita Total", "faturamento_lojas")

        total_vendas_loja_df = analise_lojas.total_vendas_por_loja()
        gerar_grafico(total_vendas_loja_df, "Total de Produtos Vendidos por Loja", "Loja", "Quantidade", "vendas_lojas")

        ticket_medio_loja_df = analise_lojas.media_ticket_loja()
        gerar_grafico(ticket_medio_loja_df, "Média de Venda por Loja", "Loja", "Ticket Médio", "ticket_medio_lojas")

        logger.info("Todas as análises foram geradas com sucesso!")
    except Exception as e:
        logger.error(f"Não foi possivel gerar todas as analises, erro: {e}")
        return

if __name__ == "__main__":
    main()
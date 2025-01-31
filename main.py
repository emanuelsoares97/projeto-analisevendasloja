from classes.classdatabasemanager import DatabaseManager
from utils.funcoes import guardar_analise_csv
from classes.classanalisevendas import AnaliseVendas  # Criar este ficheiro!

# Inicializar DatabaseManager
db_manager = DatabaseManager()

# Criar instância da classe de análises
analise = AnaliseVendas(db_manager)

# Rodar análises
receita_df = analise.calcular_receita_por_produto()
produtos_vendidos_df = analise.calcular_produtos_mais_vendidos()

# Gerar gráficos
analise.gerar_grafico(receita_df, "Top 10 Produtos com Maior Receita", "Produto", "Receita", "Top 10 Produtos com Maior Receita")
analise.gerar_grafico(produtos_vendidos_df, "Top 10 Produtos Mais Vendidos", "Produto", "Quantidade Vendida", "Top 10 Produtos Mais Vendidos")
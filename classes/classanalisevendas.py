import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from classes.classdatabasemanager import DatabaseManager
from utils.funcoes import guardar_analise_csv, logging
import os
from datetime import datetime

class AnaliseVendas:
    def __init__(self, db_manager):
        """Inicializa a classe carregando os dados do banco."""
        self.db_manager = db_manager
        self.df_produtos = db_manager.fetch_data_to_df("SELECT * FROM produtos;")
        self.df_vendas = db_manager.fetch_data_to_df("SELECT * FROM vendas;")

    def calcular_receita_por_produto(self):
        """Calcula a receita total por produto e guarda num CSV."""
        df_merged = self.df_vendas.merge(self.df_produtos, left_on="id_produto", right_on="id")
        df_merged["Receita_Venda"] = df_merged["quantidade"] * df_merged["preco"]
        receita_por_produto = df_merged.groupby("nome")["Receita_Venda"].sum().sort_values(ascending=False)
        receita_por_produto_df = receita_por_produto.reset_index()

        # Guardar CSV
        guardar_analise_csv(receita_por_produto_df, "top10_receita_por_produto")

        return receita_por_produto_df

    def calcular_produtos_mais_vendidos(self):
        """Calcula os produtos mais vendidos (quantidade total)."""
        produtos_vendidos = self.df_vendas.groupby("id_produto")["quantidade"].sum().sort_values(ascending=False)
        produtos_vendidos_df = produtos_vendidos.reset_index().merge(self.df_produtos, left_on="id_produto", right_on="id")
        produtos_vendidos_df = produtos_vendidos_df[["nome", "quantidade"]]

        # Guardar CSV
        guardar_analise_csv(produtos_vendidos_df, "top10_produtos_mais_vendidos")

        return produtos_vendidos_df


    def gerar_grafico(self, df, titulo, xlabel, ylabel, nome_ficheiro="grafico", tipo="bar"):
        """Gera um gráfico a partir de um DataFrame e salva com nome único."""

        # Criar a pasta "graficos" se não existir
        caminho_projeto = os.path.dirname(os.path.abspath(__file__))  
        caminho_data = os.path.join(caminho_projeto, "..", "graficos")  
        os.makedirs(caminho_data, exist_ok=True)  

        # Criar nome do arquivo com data e hora para evitar sobrescrita
        data_atual = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        nome_completo = os.path.join(caminho_data, f"{nome_ficheiro}_{data_atual}.png")

        # Criar figura para evitar sobreposição de gráficos
        plt.figure(figsize=(10, 5))

        # Plotar gráfico
        df.head(10).plot(kind=tipo, x="nome", ax=plt.gca())  # Usa o eixo atual para manter controle

        # Ajustes visuais
        plt.title(titulo, pad=20)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)  # Ajuste para o título não ser cortado

        # guarda o gráfico em PNG
        plt.savefig(nome_completo, dpi=300)
        
        #configuração numero eixoy
        plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(",", ".")))

        # Exibir e fechar a figura
        plt.show()
        plt.close()



import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from utils.funcoes import guardar_analise_csv, logging
import os
from datetime import datetime

class AnaliseLojas:
    def __init__(self, db_manager):
        """Inicializa a classe carregando os dados do banco."""
        self.db_manager = db_manager
        self.df_lojas = db_manager.fetch_data_to_df("SELECT * FROM lojas;")
        self.df_vendas = db_manager.fetch_data_to_df("SELECT * FROM vendas;")
        self.df_produtos = db_manager.fetch_data_to_df("SELECT * FROM produtos;")

    def total_faturado_loja(self):
        """Calcula o total gasto por cliente."""

        #juntar a tavela loja com a tabela vendas
        df_merged= self.df_lojas.merge(self.df_vendas, left_on="id_loja", right_on="id_loja")

        #juntar a tabela produto
        df_merged=df_merged.merge(self.df_produtos, left_on="id_produto", right_on="id")

        #total faturado por loja
        df_merged["Receita Total"]=df_merged["quantidade"]*df_merged["preco"]
        faturado_loja=df_merged.groupby("nome_loja")["Receita Total"].sum().sort_values(ascending=False).reset_index()
        
        # Guardar CSV
        guardar_analise_csv(faturado_loja, "total_faturado_loja")
        logging.info("Tabela guardada: total faturado por loja.")
        return faturado_loja

    def calcular_totalcompras_por_clientetop10(self):
        """Calcula a quantidade total de produtos comprados por cliente."""
        # Juntar vendas com clientes
        df_merged = self.df_vendas.merge(self.df_clientes, left_on="id_cliente", right_on="id")
        
        #clientes que mais compraram top5
        cliente_qt=df_merged.groupby("nome")["quantidade"].sum().sort_values(ascending=False).reset_index()
        cliente_qt=cliente_qt.rename(columns={"nome_x": "Cliente"}).head(10)

        # Guardar CSV
        guardar_analise_csv(cliente_qt, "top10_totalcompras_por_cliente")
        logging.info("Tabela guardada: quantidade de compras cliente.")
        return cliente_qt

    def gerar_grafico(self, df, titulo, xlabel, ylabel, nome_ficheiro="grafico", tipo="bar"):
        """Gera um gráfico a partir de um DataFrame e salva com nome único."""
        caminho_projeto = os.path.dirname(os.path.abspath(__file__))  
        caminho_data = os.path.join(caminho_projeto, "..", "graficos")  
        os.makedirs(caminho_data, exist_ok=True)  

        data_atual = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        nome_completo = os.path.join(caminho_data, f"{nome_ficheiro}_{data_atual}.png")

        plt.figure(figsize=(10, 5))

        # Verifica se "Cliente"/"quantidade" está no DataFrame antes de plotar
        if "Gasto Total" in df.columns:
            df.plot(kind=tipo, x="Cliente", y="Gasto Total", ax=plt.gca(), legend=True)
        elif "quantidade" in df.columns:
            df.plot(kind=tipo, x="Cliente", y="quantidade", ax=plt.gca(), legend=True)


        plt.title(titulo, pad=20)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)

        # Configuração do número no eixo Y
        ax = plt.gca()
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(",", ".")))
        ax.yaxis.set_major_formatter(mticker.ScalarFormatter())  # Usa ScalarFormatter
        ax.yaxis.get_major_formatter().set_scientific(False)  # Evita notação científica
        ax.yaxis.get_major_formatter().set_useOffset(False)  # Evita deslocamento automático


        plt.savefig(nome_completo, dpi=300)
        plt.show()
        plt.close()
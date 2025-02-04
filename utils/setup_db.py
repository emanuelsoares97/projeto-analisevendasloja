from classes.classdatabasemanager import DatabaseManager
from utils.logger_utils import get_logger

logger=get_logger("Setup db")

def main():
    # Inicializar o DatabaseManager
    db_manager = DatabaseManager("database/loja.db")

    # Criar tabelas no banco de dados
    db_manager.create_table()
    logger.info("Tabelas criadas com sucesso!")

    # Lista de tabelas e seus arquivos CSV correspondentes
    arquivos_csv = {
        "lojas": "./data/Lojas.csv",
        "produtos": "./data/Produtos.csv",
        "clientes": "./data/Clientes.csv",
        "vendas": "./data/Vendas.csv",
        "vendas": "./data/Atendentes.csv"
    }

    # Carregar os dados do CSV para o SQLite
    for tabela, arquivo in arquivos_csv.items():
        db_manager.load_csv_to_table(arquivo, tabela)
        logger.info(f"Dados de {tabela} carregados com sucesso!")
    logger.info("Base de dados criada e dados importados com sucesso.")

# Garantir que só roda se for executado diretamente
if __name__ == "__main__":
    main()
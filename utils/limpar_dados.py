import os
import glob
from logger_utils import logging

def limpar_base_dados():
    """Apaga a base de dados loja.db."""
    caminho_db = "database/loja.db"
    if os.path.exists(caminho_db):
        os.remove(caminho_db)
        logging.info("Base de dados apagada: loja.db")
    else:
        logging.info("Nenhuma base de dados encontrada.")

def limpar_csvs():
    """Apaga todos os ficheiros CSV antigos."""
    caminho_csvs = "./data/*.csv"
    try:
        for ficheiro in glob.glob(caminho_csvs):
            os.remove(ficheiro)
            logging.info(f"Relatório apagado: {ficheiro}")
    except Exception as e:
        logging.error(f"Erro: {e}")


def limpar_tudo():
    """Executa todas as funções de limpeza."""
    limpar_base_dados()
    limpar_csvs()
    logging.info("Todas as tabelas e database foram eliminadas!")

if __name__ == "__main__":
    limpar_tudo()
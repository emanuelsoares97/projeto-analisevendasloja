import os
import glob
from utils.logger_utils import get_logger

logger= get_logger("LimparDados")

def limpar_base_dados():
    """Apaga a base de dados loja.db."""
    caminho_db = "database/loja.db"
    if os.path.exists(caminho_db):
        os.remove(caminho_db)
        logger.info("Base de dados apagada: loja.db")
    else:
        logger.info("Nenhuma base de dados encontrada.")

def limpar_csvs():
    """Apaga todos os ficheiros CSV antigos."""
    caminho_csvs = "./data/*.csv"
    try:
        for ficheiro in glob.glob(caminho_csvs):
            os.remove(ficheiro)
            logger.info(f"Relatório apagado: {ficheiro}")
    except Exception as e:
        logger.error(f"Erro: {e}")


def limpar_tudo():
    """Executa todas as funções de limpeza com confirmação do utilizador."""
    confirmacao = input("Tens a certeza que queres apagar tudo? (s/n): ")
    if confirmacao.lower() == "s":
        limpar_base_dados()
        limpar_csvs()
        logger.info("Todas as tabelas e a base de dados foram eliminadas com sucesso!")
    else:
        logger.info("Operação cancelada pelo utilizador.")


if __name__ == "__main__":
    limpar_tudo()
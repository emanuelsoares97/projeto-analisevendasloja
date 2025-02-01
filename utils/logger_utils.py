import os
import logging

# Criar diretório para logs se não existir
caminho_projeto = os.path.dirname(os.path.abspath(__file__))  # Caminho do logger_utils.py
caminho_raiz = os.path.join(caminho_projeto, "..")  # Diretório raiz do projeto
caminho_logs = os.path.join(caminho_raiz, "logs")  # Criar pasta logs no mesmo nível do main.py
os.makedirs(caminho_logs, exist_ok=True)  # Criar diretório se não existir

# Caminho do ficheiro de log
caminho_log = os.path.join(caminho_logs, "projeto_analise.log")

# Configuração global do logging
logging.basicConfig(
    filename=caminho_log,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    encoding="utf-8"
)

# Função para criar um logger específico para cada classe/módulo
def get_logger(nome):
    """Cria e retorna um logger específico para uma classe/módulo."""
    logger = logging.getLogger(nome)
    return logger



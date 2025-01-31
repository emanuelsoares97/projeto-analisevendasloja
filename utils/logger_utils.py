import os
import logging

# Obter o diretório onde está o `main.py`
caminho_projeto = os.path.dirname(os.path.abspath(__file__))  # Caminho do `logger_utils.py`
caminho_raiz = os.path.join(caminho_projeto, "..")  # Sobe um nível para o diretório raiz
caminho_log = os.path.join(caminho_raiz, "log.txt")  # Garante que o log fica no mesmo nível do `main.py`

# Configuração do logging
logging.basicConfig(
    filename=caminho_log,  # Caminho correto para guardar o log
    level=logging.INFO,  # Define o nível de logging
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    encoding="utf-8"
)


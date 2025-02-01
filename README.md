# Projeto Análise de Loja

## Descrição

O **Projeto Análise de Vendas** é um sistema de análise de dados que extrai informações de uma base de dados SQL e utiliza a biblioteca **Pandas** para tratamento e visualização dos dados. O objetivo principal é gerar insights a partir das vendas, identificando padrões como:

**Receita total** por produto, loja e atendente  
**Produtos mais vendidos**  
**Clientes com maior volume de compras**  
**Atendentes com maior faturamento**  

Além disso, o projeto gera **gráficos automatizados** e **relatórios CSV**, tornando a análise mais visual e acessível.

---

## **Tecnologias Utilizadas**

- **Python 3.10+**  
- **Pandas** – Manipulação e análise de dados  
- **Matplotlib** – Geração de gráficos  
- **SQLite** – Base de dados  
- **Logging** – Monitoramento do processo  
- **Jupyter Notebooks** – Testes e exploração inicial  

---

## 📂 **Estrutura do Projeto**

meu-projeto-de-vendas/
├── README.md  # Explicação do projeto
├── classes/
│   ├── DatabaseManager
│   ├── ClientesManager
│   ├── VendasManager
│   ├── LojasManager
├── database/
│   ├── loja.db  # Arquivo SQLite (pode ser incluído ou gerado pelo código)
│   └── scripts.sql  # Opcional: scripts para criar tabelas ainda nao sei se vou fazer
├── graficos/ #graficos gerados automaticamente pelas analises feitas guardados em png
├── data/
│   ├── vendas.csv 
│   └── produtos.csv
│   └── analisescsv/ #ficam os dados gerados em csv pelas analises feitas
├── notebooks/
│   ├── analise_vendas.ipynb  # Notebook com a análise em Pandas
│   ├── analise_receita.ipynb  # Notebook com a análise em Pandas
│   ├── analise_clientes.ipynb  # Notebook com a análise em Pandas
│   ├── analise_lojas.ipynb  # Notebook com a análise em Pandas
├── main.py  # Script principal
└── requirements.txt  # Bibliotecas Python usadas no projeto


import pandas as pd
from pathlib import Path

# definindo a rota para acessar a pasta /data
PASTA_RAIZ = Path(__file__).resolve().parent.parent
PASTA_DATA = PASTA_RAIZ / "data"

# função para carregar tabela
def carregar_tabela(nome_arquivo):
    return pd.read_csv(
        PASTA_DATA / nome_arquivo,
        sep=";"
    )

# funções para carregar cada uma das tabelas do dataset
def tabela_avaliacao():
    return carregar_tabela("tabela_avaliacao.csv")

def tabela_clientes():
    return carregar_tabela("tabela_clientes.csv")

def tabela_itens():
    return carregar_tabela("tabela_itens.csv")

def tabela_pagamentos():
    return carregar_tabela("tabela_pagamentos.csv")

def tabela_pedidos():
    return carregar_tabela("tabela_pedidos.csv")

def tabela_produtos():
    return carregar_tabela("tabela_produtos.csv")
# %%

# IMPORTANDO PANDAS E PATH
import pandas as pd
from pathlib import Path

# %%

# DEFININDO A ROTA
PASTA_RAIZ = Path(__file__).resolve().parent.parent
PASTA_DATA = PASTA_RAIZ / "data"


# %%

# CRIANDO FUNÇÕES PARA CARREAGAR TABELAS
def tabela_avaliacao():
    avaliacao = pd.read_csv(PASTA_DATA / 'Tabela_Avaliacao.csv', sep= ';')
    return avaliacao

def tabela_clientes():
    clientes = pd.read_csv(PASTA_DATA / 'Tabela_Clientes.csv', sep= ';')
    return clientes

def tabela_itens():
    itens = pd.read_csv(PASTA_DATA / 'Tabela_Itens.csv', sep= ';')
    return itens

def tabela_pagamentos():
    pagamentos = pd.read_csv(PASTA_DATA / 'Tabela_Pagamentos.csv', sep= ';')
    return pagamentos

def tabela_pedidos():
    pedidos = pd.read_csv(PASTA_DATA / 'Tabela_Pedidos.csv', sep= ';')
    return pedidos

def tabela_produtos():
    produtos = pd.read_csv(PASTA_DATA / 'Tabela_Produtos.csv', sep= ';')
    return produtos
# %%

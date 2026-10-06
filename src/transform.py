# %%
import pandas as pd
from extract import tabela_avaliacao, tabela_clientes, tabela_itens, tabela_pagamentos, tabela_pedidos, tabela_produtos

# %%
# CARREGAR TABELAS
avaliacao = tabela_avaliacao()
pagamentos = tabela_pagamentos()

pedidos = tabela_pedidos()
clientes = tabela_clientes()

itens = tabela_itens()
produtos = tabela_produtos()
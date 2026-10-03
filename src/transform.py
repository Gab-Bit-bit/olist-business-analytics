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



# %%

# Conhecer a estrutura
print("PAGAMENTOS")
print("Linhas e colunas:", pagamentos.shape)

print("\nPRIMEIRAS LINHAS:")
print(pagamentos.head().to_string(index=False))

print("\nTIPOS E VALORES NÃO NULOS:")
pagamentos.info()

# %%

# Verificar nulos e duplicatas
print("NULOS POR COLUNA:")
print(pagamentos.isna().sum())

print("\nPedidos distintos:", pagamentos["order_id"].nunique())

print("Repetições completas além da primeira:",
      pagamentos.duplicated().sum())

print("Repetições de pedido + sequência:",
      pagamentos.duplicated(
          subset=["order_id", "payment_sequential"]
      ).sum())

# %%

# Examinar valores e formas de pagamento
print("ESTATÍSTICAS NUMÉRICAS:")
print(pagamentos.describe().to_string())

print("\nFORMAS DE PAGAMENTO:")
print(pagamentos["payment_type"].value_counts(dropna=False))

# %%

# Investigar valores incomuns
valor_zero = pagamentos[pagamentos["payment_value"] == 0]

parcelas_zero = pagamentos[
    pagamentos["payment_installments"] == 0
]

tipo_indefinido = pagamentos[
    pagamentos["payment_type"] == "not_defined"
]

print("PAGAMENTOS COM VALOR ZERO:")
print(valor_zero.to_string(index=False))

print("\nPAGAMENTOS COM ZERO PARCELAS:")
print(parcelas_zero.to_string(index=False))

print("\nPAGAMENTOS COM TIPO NÃO DEFINIDO:")
print(tipo_indefinido.to_string(index=False))

# %%

# Investigar os pedidos com algum pagamento zero
pedidos_com_zero = valor_zero["order_id"].unique()

pagamentos_desses_pedidos = pagamentos[
    pagamentos["order_id"].isin(pedidos_com_zero)
]

resumo_pedidos_zero = pagamentos_desses_pedidos.groupby("order_id").agg(
    quantidade_registros=("payment_value", "size"),
    valor_total_pago=("payment_value", "sum")
)

print("RESUMO DOS PEDIDOS COM ALGUM PAGAMENTO ZERO:")
print(resumo_pedidos_zero.to_string())



# %%

# Conhecer a estrutura
print("AVALIAÇÃO")
print("Linhas e colunas:", avaliacao.shape)

print("\nPRIMEIRAS LINHAS:")
print(avaliacao.head().to_string(index=False))

print("\nTIPOS E VALORES NÃO NULOS:")
avaliacao.info()

# %%

# Verificar nulos e duplicatas
print("NULOS POR COLUNA:")
print(avaliacao.isna().sum())

print("\nPedidos distintos:", avaliacao["order_id"].nunique())

print("Repetições completas além da primeira:",
      avaliacao.duplicated().sum())

# %%

# Examinar as notas
print("ESTATÍSTICAS DAS NOTAS:")
print(avaliacao["review_score"].describe())

print("\nDISTRIBUIÇÃO DAS NOTAS:")
print(
    avaliacao["review_score"]
    .value_counts(dropna=False)
    .sort_index()
)

notas_invalidas = avaliacao[
    avaliacao["review_score"].notna()
    & ~avaliacao["review_score"].isin([1, 2, 3, 4, 5])
]

print("\nQuantidade de notas fora dos valores permitidos:",
      len(notas_invalidas))

# %%

# Investigar pedidos com várias avaliações
resumo_avaliacoes = avaliacao.groupby("order_id").agg(
    quantidade_avaliacoes=("review_score", "size"),
    notas_distintas=("review_score", "nunique")
)

multiplas_avaliacoes = resumo_avaliacoes[
    resumo_avaliacoes["quantidade_avaliacoes"] > 1
]

mesma_nota = multiplas_avaliacoes[
    multiplas_avaliacoes["notas_distintas"] == 1
]

notas_diferentes = multiplas_avaliacoes[
    multiplas_avaliacoes["notas_distintas"] > 1
]

print("Pedidos com várias avaliações:", len(multiplas_avaliacoes))
print("Pedidos com várias avaliações e a mesma nota:", len(mesma_nota))
print("Pedidos com notas diferentes:", len(notas_diferentes))

# %%

# Mostrar exemplos de notas diferentes
exemplos = avaliacao[
    avaliacao["order_id"].isin(notas_diferentes.head(3).index)
]

print("EXEMPLOS DE PEDIDOS COM NOTAS DIFERENTES:")
print(exemplos.sort_values("order_id").to_string(index=False))
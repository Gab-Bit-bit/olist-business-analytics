import pandas as pd
import transform_config
from extract import tabela_pagamentos

pagamentos = tabela_pagamentos()

'''
1 - AUDITORIA/ANÁLISE

'''

# conhecer a estrutura
print("PAGAMENTOS")
print("Linhas e colunas:", pagamentos.shape)

print("\nPRIMEIRAS LINHAS:")
print(pagamentos.head().to_string(index=False))

print("\nTIPOS E VALORES NÃO NULOS:")
pagamentos.info()


# verificar nulos e duplicatas
print("NULOS POR COLUNA:")
print(pagamentos.isna().sum())

print("\nPedidos distintos:", pagamentos["order_id"].nunique())

print("Repetições completas além da primeira:",
      pagamentos.duplicated().sum())

print("Repetições de pedido + sequência:",
      pagamentos.duplicated(
          subset=["order_id", "payment_sequential"]
      ).sum())


# examinar valores e formas de pagamento
print("ESTATÍSTICAS NUMÉRICAS:")
print(pagamentos.describe().to_string())

print("\nFORMAS DE PAGAMENTO:")
print(pagamentos["payment_type"].value_counts(dropna=False))


# investigar valores incomuns
valor_zero = pagamentos[pagamentos["payment_value"] == 0]

parcelas_zero = pagamentos[
    pagamentos["payment_installments"] == 0
]

tipo_indefinido = pagamentos[
    pagamentos["payment_type"] == "not_defined"
]

print("\nPAGAMENTOS COM VALOR ZERO:")
print(valor_zero.to_string(index=False))

print("\nPAGAMENTOS COM ZERO PARCELAS:")
print(parcelas_zero.to_string(index=False))

print("\nPAGAMENTOS COM TIPO NÃO DEFINIDO:")
print(tipo_indefinido.to_string(index=False))


# investigar os pedidos com algum pagamento zero
pedidos_com_zero = valor_zero["order_id"].unique()

pagamentos_desses_pedidos = pagamentos[
    pagamentos["order_id"].isin(pedidos_com_zero)
]

resumo_pedidos_zero = pagamentos_desses_pedidos.groupby("order_id").agg(
    quantidade_registros=("payment_value", "size"),
    valor_total_pago=("payment_value", "sum")
)

print("\nRESUMO DOS PEDIDOS COM ALGUM PAGAMENTO ZERO:")
print(resumo_pedidos_zero.to_string())

'''
2 - TRATAMENTO

'''

# CRIAR A BASE TRATADA E AJUSTAR OS TIPOS

# cria uma cópia para preservar a tabela original
pagamentos_tratados = pagamentos.copy()

pagamentos_tratados = pagamentos_tratados.astype({
    "order_id": "string",
    "payment_sequential": "Int64",
    "payment_type": "string",
    "payment_installments": "Int64",
    "payment_value": "float64"
})

# TRATAR E SINALIZAR OS CASOS IDENTIFICADOS

# sinaliza pagamentos com valor zero, sem excluir eles
pagamentos_tratados["pagamento_valor_zero"] = (
    pagamentos_tratados["payment_value"] == 0
)

# identifica o problema antes de alterar a quantidade de parcelas
pagamentos_tratados["parcelas_inconsistentes"] = (
    (pagamentos_tratados["payment_type"] == "credit_card")
    & (pagamentos_tratados["payment_installments"] == 0)
)

# zero parcelas no cartão passa a representar informação desconhecida
pagamentos_tratados.loc[
    pagamentos_tratados["parcelas_inconsistentes"],
    "payment_installments"
] = pd.NA

# tipo não definido passa a ser representado como informação ausente
pagamentos_tratados.loc[
    pagamentos_tratados["payment_type"] == "not_defined",
    "payment_type"
] = pd.NA

# CONFERIR O RESULTADO

print("\nLinhas antes:", len(pagamentos))
print("Linhas depois:", len(pagamentos_tratados))

print("\nNULOS APÓS O TRATAMENTO:")
print(pagamentos_tratados.isna().sum())

print("\nPAGAMENTOS SINALIZADOS:")
print(
    pagamentos_tratados[
        ["pagamento_valor_zero", "parcelas_inconsistentes"]
    ].sum()
)

print("\nTIPOS APÓS O TRATAMENTO:")
print(pagamentos_tratados.dtypes)

'''

Resumo:

A tabela de pagamentos apresentou 103.886 registros, 
sem valores nulos ou duplicatas completas na base original. 
Foram identificados 9 pagamentos com valor zero, 
2 registros de cartão de crédito com zero parcelas e 
3 registros com tipo `not_defined`.

Os pagamentos com valor zero foram preservados e 
sinalizados porque não indicam, necessariamente, um erro. 
Dos 9 registros, 6 são vouchers de pedidos que também possuem pagamentos positivos. 
Os outros 3 possuem tipo indefinido e 
precisam ser investigados junto à tabela de pedidos antes de qualquer exclusão.

Nos pagamentos por cartão com zero parcelas, 
a quantidade de parcelas foi substituída por valor ausente, 
pois não há informação suficiente para determinar a quantidade correta. 
O tipo `not_defined` também foi convertido em valor ausente, 
representando explicitamente uma informação desconhecida.

Os tipos das colunas foram padronizados conforme sua finalidade: 
identificadores como texto, sequências e parcelas como inteiros e 
valores pagos como números decimais. Para parcelas, 
foi utilizado um tipo inteiro que aceita valores ausentes.

Nenhuma linha foi excluída. 
Os pagamentos de um mesmo pedido foram mantidos porque um pedido pode ter mais de um pagamento, 
e não foram encontradas repetições da combinação `order_id` e 
`payment_sequential`. O tratamento foi realizado em uma cópia, 
preservando os dados originais para conferência.

'''
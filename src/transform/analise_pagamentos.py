import transform_config
from extract import tabela_pagamentos
pagamentos = tabela_pagamentos()


# Conhecer a estrutura
print("PAGAMENTOS")
print("Linhas e colunas:", pagamentos.shape)

print("\nPRIMEIRAS LINHAS:")
print(pagamentos.head().to_string(index=False))

print("\nTIPOS E VALORES NÃO NULOS:")
pagamentos.info()


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


# Examinar valores e formas de pagamento
print("ESTATÍSTICAS NUMÉRICAS:")
print(pagamentos.describe().to_string())

print("\nFORMAS DE PAGAMENTO:")
print(pagamentos["payment_type"].value_counts(dropna=False))


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
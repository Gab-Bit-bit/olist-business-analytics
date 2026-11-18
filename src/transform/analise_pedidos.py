import pandas as pd
import transform_config
from extract import tabela_pedidos

pedidos = tabela_pedidos()

'''
1 - AUDITORIA/ANÁLISE

'''

# conhecer a estrutura
print("PEDIDOS")
print("Linhas e colunas:", pedidos.shape)

print("\nPRIMEIRAS LINHAS:")
print(pedidos.head().to_string(index=False))

print("\nTIPOS E VALORES NÃO NULOS:")
pedidos.info()


# verificar nulos e duplicatas
print("\nNULOS POR COLUNA:")
print(pedidos.isna().sum())

print("\nRepetições completas além da primeira:",
      pedidos.duplicated().sum())

print("Repetições de order_id:",
      pedidos["order_id"].duplicated().sum())

print("Repetições de customer_id:",
      pedidos["customer_id"].duplicated().sum())


# examinar os status
print("\nSTATUS DOS PEDIDOS:")
print(pedidos["order_status"].value_counts(dropna=False))


# verificar as datas
colunas_datas = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

# converte apenas para conferência, sem alterar a tabela original
datas = pedidos[colunas_datas].apply(pd.to_datetime, errors="coerce")

datas_invalidas = datas.isna() & pedidos[colunas_datas].notna()

print("\nDATAS QUE NÃO PUDERAM SER CONVERTIDAS:")
print(datas_invalidas.sum())

print("\nINTERVALO DAS DATAS:")
print(datas.agg(["min", "max"]).T.to_string())

entrega_antes_compra = pedidos[
    datas["order_delivered_customer_date"]
    < datas["order_purchase_timestamp"]
]

previsao_antes_compra = pedidos[
    datas["order_estimated_delivery_date"].dt.normalize()
    < datas["order_purchase_timestamp"].dt.normalize()
]

print("\nEntregas anteriores à compra:", len(entrega_antes_compra))
print("Previsões anteriores à compra:", len(previsao_antes_compra))


# cruzar status e data de entrega
sem_data_entrega = pedidos["order_delivered_customer_date"].isna()

print("\nSTATUS x AUSÊNCIA DA DATA DE ENTREGA:")
print(pd.crosstab(
    pedidos["order_status"],
    sem_data_entrega.rename("sem_data_entrega")
))

# pedido entregue precisa ter data de entrega
entregue_sem_data = pedidos[
    (pedidos["order_status"] == "delivered") & sem_data_entrega
]

# pedido não entregue não deveria ter data de entrega
nao_entregue_com_data = pedidos[
    (pedidos["order_status"] != "delivered") & ~sem_data_entrega
]

# ausência esperada: pedido ainda não entregue ou que não será entregue
ausencia_esperada = pedidos[
    (pedidos["order_status"] != "delivered") & sem_data_entrega
]

print("\nAusências esperadas da data de entrega:", len(ausencia_esperada))
print("Entregues sem data de entrega:", len(entregue_sem_data))
print("Não entregues com data de entrega:", len(nao_entregue_com_data))

print("\nPEDIDOS ENTREGUES SEM DATA DE ENTREGA:")
print(entregue_sem_data.to_string(index=False))

print("\nPEDIDOS NÃO ENTREGUES COM DATA DE ENTREGA:")
print(nao_entregue_com_data.to_string(index=False))

'''

Resumo:

A tabela de pedidos apresentou 99.441 registros, 
sem duplicatas completas e sem repetições de `order_id` ou `customer_id`. 
Todas as colunas foram carregadas como texto, inclusive as datas, 
que puderam ser convertidas sem erros. 
Não há entregas nem previsões anteriores à data da compra.

A única coluna com ausências é a data de entrega ao cliente, com 2.965 nulos. 
Desses, 2.957 são esperados, pois pertencem a pedidos que ainda não foram entregues 
ou que não serão entregues (enviados, cancelados, indisponíveis, faturados, 
em processamento, criados ou aprovados). 
Foram identificadas 14 inconsistências entre status e data de entrega: 
8 pedidos com status `delivered` sem data de entrega e 
6 pedidos com status `canceled` que possuem data de entrega.

Tratamentos recomendados, ainda não aplicados:
- converter as três colunas de data para datetime, `order_id` e `customer_id` 
  para texto e `order_status` para texto ou categoria;
- manter como ausentes as 2.957 datas de entrega esperadas, sem preencher;
- sinalizar os 8 pedidos entregues sem data, sem inventar uma data de entrega, 
  e excluí-los do cálculo de atraso;
- sinalizar os 6 pedidos cancelados com data de entrega, sem alterar o status, 
  e excluí-los da análise de atraso até que sejam investigados;
- calcular o atraso apenas com pedidos `delivered` que tenham data de entrega, 
  comparando as datas no nível do dia, pois a previsão não registra horário.

Entregas posteriores à previsão não foram tratadas como erro de qualidade, 
pois representam o atraso que será objeto da análise.

'''

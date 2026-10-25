import pandas as pd
import transform_config
from extract import tabela_itens

itens = tabela_itens()

'''
1 - AUDITORIA/ANÁLISE

'''

#CONVERSÃO PARA DATETIME
itens["shipping_limit_date"] = pd.to_datetime(itens["shipping_limit_date"])


#CONVERSÃO DE PREÇO E FRETE PARA NUMÉRICO
itens['price'] = pd.to_numeric(itens['price'], errors='coerce')
itens['freight_value'] = pd.to_numeric(itens['freight_value'], errors='coerce')


#REMOVE LINHAS DUPLICADAS
print(f"Duplicatas antes: {itens.duplicated().sum()}")
itens = itens.drop_duplicates()


#REMOVE LINHAS ONDE PREÇO OU FRETE SÃO NULOS
print("\nNulos por coluna antes do tratamento:")
print(itens.isnull().sum())
itens = itens.dropna(subset=['price', 'freight_value'])


#CRIA COLUNA DE VALOR TOTAL
itens['total_value'] = itens['price'] + itens['freight_value']


#EXIBE ESTATISTICAS
print("\nESTATÍSTICAS:")
print(itens.describe().to_string())

'''

Resumo:

A tabela de itens apresentou 112.650 registros, 
sem linhas duplicadas e sem valores nulos em preço ou frete. 
Por isso, a remoção de duplicatas e de nulos não excluiu nenhuma linha. 
O preço e o frete já são carregados como números decimais, 
então a conversão para numérico não alterou os valores 
e funciona apenas como proteção. 
A data limite de envio foi convertida para data, 
e foi criada a coluna `total_value`, que soma preço e frete.

As estatísticas mostram preços entre 0,85 e 6.735,00 e 
até 21 itens em um mesmo pedido. 
Foram observados dois pontos que ainda não foram tratados:
- 383 itens com frete zero, que podem representar frete grátis 
  e não indicam, necessariamente, um erro;
- 4 itens com data limite de envio em 2020, 
  posterior à última compra registrada na tabela de pedidos (outubro de 2018), 
  o que indica uma provável inconsistência de data.

Tratamentos recomendados, ainda não aplicados:
- sinalizar os itens com frete zero, sem excluí-los;
- sinalizar os 4 itens com data limite de envio em 2020 
  e investigá-los junto à tabela de pedidos.

Diferentemente das tabelas de pagamentos e avaliações, 
o tratamento foi aplicado diretamente na tabela carregada, sem criar uma cópia.

'''

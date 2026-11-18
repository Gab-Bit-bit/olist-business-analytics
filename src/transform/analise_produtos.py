import pandas as pd
import transform_config
from extract import tabela_produtos

produtos = tabela_produtos()

'''
1 - AUDITORIA/ANÁLISE

'''

#CONVERTE DIMENSÕES E PESO DO PRODUTO PARA NUMÉRICO
colunas_medidas = ['product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']

for col in colunas_medidas:
    produtos[col] = pd.to_numeric(produtos[col], errors='coerce')


#VERIFICA SE A CONVERSÃO FUNCIONOU
print("TIPOS APÓS A CONVERSÃO:")
print(produtos.dtypes)


#PREENCHE PRODUTOS SEM CATEGORIA COM O TEXTO 'nao_definido'
produtos['product_category_name'] = produtos['product_category_name'].fillna('nao_definido')


#CHECA NULOS
print("\nNULOS POR COLUNA:")
print(produtos.isnull().sum())


#CHECA IDS DUPLICADOS
print("\nIDs duplicados:", produtos['product_id'].duplicated().sum())


#EXIBE ESTATISTICAS DESCRITIVA DAS MEDIDAS DOS PRODUTOS
print("\nESTATÍSTICAS DAS MEDIDAS:")
print(produtos[colunas_medidas].describe().to_string())


#EXIBE O TOTAL DE CATEGORIAS UNICAS
print("\nCategorias únicas:", produtos['product_category_name'].nunique())


#EXIBE AS 10 CATEGORIAS MAIS FREQUENTES
print("\n10 CATEGORIAS MAIS FREQUENTES:")
print(produtos['product_category_name'].value_counts().head(10))

'''

Resumo:

A tabela de produtos apresentou 32.951 registros, 
sem repetições de `product_id`. 
As medidas de peso e dimensões já são carregadas como números decimais, 
então a conversão para numérico não alterou os valores 
e funciona apenas como proteção.

Foram encontrados 610 produtos sem categoria, 
que foram preenchidos com o texto `nao_definido`. 
Como a verificação de nulos é feita depois desse preenchimento, 
essas ausências não aparecem na contagem exibida pelo script. 
Após o preenchimento, existem 74 categorias: 
73 originais e a categoria `nao_definido`. 
A categoria mais frequente é `cama_mesa_banho`, com 3.029 produtos.

Também foram observados pontos que ainda não foram tratados:
- 2 produtos sem nenhuma medida de peso ou dimensão, 
  sendo que um deles também não possui categoria;
- 4 produtos com peso zero, todos da categoria `cama_mesa_banho` 
  e com as mesmas dimensões (30 x 25 x 30 cm), 
  o que indica um provável erro de cadastro.

Tratamentos recomendados, ainda não aplicados:
- manter como ausentes as medidas dos 2 produtos, sem preencher;
- tratar o peso zero como informação ausente ou sinalizá-lo, 
  pois um produto não pode ter peso zero.

Diferentemente das tabelas de pagamentos e avaliações, 
o tratamento foi aplicado diretamente na tabela carregada, sem criar uma cópia.

'''

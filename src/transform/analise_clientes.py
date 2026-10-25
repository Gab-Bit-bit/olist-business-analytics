import pandas as pd
import transform_config
from extract import tabela_clientes

clientes = tabela_clientes()

'''
1 - AUDITORIA/ANÁLISE

'''

# conhecer a estrutura
print("CLIENTES")
print("Linhas e colunas:", clientes.shape)

print("\nPRIMEIRAS LINHAS:")
print(clientes.head().to_string(index=False))

print("\nTIPOS E VALORES NÃO NULOS:")
clientes.info()


# verificar nulos e textos vazios
print("\nNULOS POR COLUNA:")
print(clientes.isna().sum())

# texto vazio ou contendo apenas espaços
textos_vazios = clientes.apply(
    lambda coluna: coluna.str.strip().eq("") & coluna.notna()
)

print("\nTEXTOS VAZIOS OU APENAS COM ESPAÇOS:")
print(textos_vazios.sum())


# verificar duplicatas
print("\nRepetições completas além da primeira:",
      clientes.duplicated().sum())

# separa repetições de customer_id idênticas das que trazem informações diferentes
repeticoes_customer_id = clientes[
    clientes.duplicated(subset=["customer_id"], keep=False)
]

customer_id_conflitante = repeticoes_customer_id.groupby("customer_id").filter(
    lambda grupo: len(grupo.drop_duplicates()) > 1
)

print("Repetições de customer_id além da primeira:",
      clientes["customer_id"].duplicated().sum())
print("customer_id repetidos com registros idênticos:",
      repeticoes_customer_id["customer_id"].nunique()
      - customer_id_conflitante["customer_id"].nunique())
print("customer_id repetidos com informações conflitantes:",
      customer_id_conflitante["customer_id"].nunique())


# investigar repetições de customer_unique_id
# o mesmo cliente pode ter um customer_id diferente em cada pedido
resumo_unique_id = clientes.groupby("customer_unique_id").agg(
    quantidade_registros=("customer_id", "size"),
    cidades_distintas=("customer_city", "nunique"),
    estados_distintos=("customer_state", "nunique")
)

unique_id_repetidos = resumo_unique_id[
    resumo_unique_id["quantidade_registros"] > 1
]

print("\nClientes únicos (customer_unique_id):", len(resumo_unique_id))
print("Clientes com mais de um registro:", len(unique_id_repetidos))
print("Registros desses clientes:",
      unique_id_repetidos["quantidade_registros"].sum())
print("Clientes com mais de uma cidade:",
      (unique_id_repetidos["cidades_distintas"] > 1).sum())
print("Clientes com mais de um estado:",
      (unique_id_repetidos["estados_distintos"] > 1).sum())

print("\nDISTRIBUIÇÃO DE REGISTROS POR CLIENTE:")
print(resumo_unique_id["quantidade_registros"].value_counts().sort_index())


# verificar variações de espaços e capitalização
for coluna in ["customer_city", "customer_state"]:
    valores = clientes[coluna]

    # forma padronizada usada apenas para comparação
    padronizado = valores.str.strip().str.replace(r"\s+", " ", regex=True)

    print(f"\n{coluna.upper()}:")
    print("Valores distintos:", valores.nunique())
    print("Distintos após padronizar espaços e capitalização:",
          padronizado.str.lower().nunique())
    print("Registros com espaços no início ou no fim:",
          (valores != valores.str.strip()).sum())
    print("Registros com espaços repetidos:",
          valores.str.contains(r"\s{2,}", regex=True).sum())
    print("Registros em minúsculas:", (valores == valores.str.lower()).sum())
    print("Registros em maiúsculas:", (valores == valores.str.upper()).sum())


# verificar UFs válidas
ufs_validas = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]

ufs_invalidas = clientes[~clientes["customer_state"].isin(ufs_validas)]

print("\nRegistros com UF inválida:", len(ufs_invalidas))
print("UFs presentes:", clientes["customer_state"].nunique(), "de", len(ufs_validas))

print("\nCLIENTES POR ESTADO:")
print(clientes["customer_state"].value_counts())

'''

Resumo:

A tabela de clientes apresentou 99.441 registros e 4 colunas, 
todas carregadas como texto. Não foram encontrados valores nulos, 
textos vazios ou contendo apenas espaços, nem linhas completamente duplicadas. 
O `customer_id` não se repete, portanto não há registros idênticos 
nem informações conflitantes para o mesmo identificador.

Foram identificados 96.096 clientes únicos (`customer_unique_id`). 
Desses, 2.997 aparecem em mais de um registro, somando 6.342 linhas. 
Isso não indica erro, pois cada pedido gera um `customer_id` diferente 
para o mesmo cliente. Entre esses clientes, 122 aparecem em mais de uma cidade 
e 39 em mais de um estado, o que pode representar mudança de endereço 
ou entregas em locais diferentes.

As colunas `customer_city` e `customer_state` já estão padronizadas: 
não há espaços no início, no fim ou repetidos, as cidades estão 
todas em minúsculas e os estados todos em maiúsculas. 
Os 27 valores de UF são válidos e cobrem todos os estados e o Distrito Federal.

Tratamentos recomendados, ainda não aplicados:
- padronizar os identificadores e a cidade como texto e 
  `customer_state` como categoria;
- não remover nem agrupar as repetições de `customer_unique_id`;
- usar `customer_id` como chave de ligação com a tabela de pedidos, 
  atribuindo a cada pedido o estado registrado naquele pedido;
- caso a análise seja feita por cliente, e não por pedido, 
  definir uma regra para os 39 clientes com mais de um estado;
- manter a limpeza de espaços e capitalização no fluxo de tratamento 
  como proteção, embora não altere nenhum registro atual.

'''

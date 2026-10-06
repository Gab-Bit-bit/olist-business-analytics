import transform_config
from extract import tabela_avaliacao

avaliacao = tabela_avaliacao()

'''
1 - AUDITORIA/ANÁLISE

'''

# conhecer a estrutura
print("AVALIAÇÃO")
print("Linhas e colunas:", avaliacao.shape)

print("\nPRIMEIRAS LINHAS:")
print(avaliacao.head().to_string(index=False))

print("\nTIPOS E VALORES NÃO NULOS:")
avaliacao.info()


# verificar nulos e duplicatas
print("\nNULOS POR COLUNA:")
print(avaliacao.isna().sum())

print("\nPedidos distintos:", avaliacao["order_id"].nunique())

print("Repetições completas além da primeira:",
      avaliacao.duplicated().sum())


# examinar as notas
print("\nESTATÍSTICAS DAS NOTAS:")
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


# investigar pedidos com várias avaliações
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


# mostrar exemplos de notas diferentes
exemplos = avaliacao[
    avaliacao["order_id"].isin(notas_diferentes.head(3).index)
]

print("\nEXEMPLOS DE PEDIDOS COM NOTAS DIFERENTES:")
print(exemplos.sort_values("order_id").to_string(index=False))

'''
2 - TRATAMENTO

'''

# CRIAR A BASE TRATADA

# cria uma cópia para preservar a tabela original
avaliacao_tratada = avaliacao.copy()

avaliacao_tratada = avaliacao_tratada.astype({
    "order_id": "string",
    "review_score": "Int64"
})

# SINALIZAR AS REPETIÇÕES

# marca todos os registros de pedidos com mais de uma avaliação
avaliacao_tratada["pedido_com_multiplas_avaliacoes"] = (
    avaliacao_tratada.duplicated(
        subset=["order_id"],
        keep=False
    )
)

# marca todos os registros que repetem a combinação pedido + nota
avaliacao_tratada["pedido_nota_repetidos"] = (
    avaliacao_tratada.duplicated(
        subset=["order_id", "review_score"],
        keep=False
    )
)

# CONFERIR O RESULTADO

print("Linhas antes:", len(avaliacao))
print("Linhas depois:", len(avaliacao_tratada))

print("\nNULOS APÓS O TRATAMENTO:")
print(avaliacao_tratada.isna().sum())

print("\nTIPOS APÓS O TRATAMENTO:")
print(avaliacao_tratada.dtypes)

pedidos_multiplos = avaliacao_tratada.loc[
    avaliacao_tratada["pedido_com_multiplas_avaliacoes"],
    "order_id"
].nunique()

print("\nPedidos com várias avaliações:", pedidos_multiplos)

print(
    "Repetições de pedido + nota além da primeira:",
    avaliacao_tratada.duplicated(
        subset=["order_id", "review_score"]
    ).sum()
)

'''

Resumo:

A tabela de avaliações apresentou 99.224 registros, 
sem valores nulos e com todas as notas entre 1 e 5. 
Foram identificados 547 pedidos com múltiplas avaliações: 
345 com notas iguais e 202 com notas diferentes. 
Também foram encontradas 349 repetições da combinação de pedido e 
nota além da primeira ocorrência.

O identificador do pedido foi padronizado como texto, 
pois representa uma identificação, e não uma quantidade. 
A nota foi padronizada como número inteiro, 
pois seus valores são discretos, de 1 a 5. 
Como não foram identificadas notas inválidas ou ausentes, 
não houve necessidade de corrigir ou preencher esses valores.

As repetições foram preservadas e 
sinalizadas porque a tabela contém apenas `order_id` e `review_score`. 
Duas avaliações distintas podem pertencer ao mesmo pedido e 
receber a mesma nota, tornando-se iguais nessas duas colunas. 
Sem o identificador da avaliação e suas datas, 
não é possível distinguir com segurança uma avaliação diferente de um registro duplicado indevidamente. 
Também não é possível determinar qual avaliação é a mais recente quando há notas diferentes.

Nenhuma linha foi excluída, 
evitando a perda de registros potencialmente legítimos. 
As sinalizações permitem localizar esses casos para investigação. 
Antes de calcular indicadores por pedido ou integrar as tabelas, 
será necessário definir uma regra para múltiplas avaliações, 
evitando que alguns pedidos tenham peso maior na análise. 
O tratamento foi realizado em uma cópia, preservando a base original.

'''
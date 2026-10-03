import transform_config
from extract import tabela_avaliacao
avaliacao = tabela_avaliacao()


# Conhecer a estrutura
print("AVALIAÇÃO")
print("Linhas e colunas:", avaliacao.shape)

print("\nPRIMEIRAS LINHAS:")
print(avaliacao.head().to_string(index=False))

print("\nTIPOS E VALORES NÃO NULOS:")
avaliacao.info()


# Verificar nulos e duplicatas
print("NULOS POR COLUNA:")
print(avaliacao.isna().sum())

print("\nPedidos distintos:", avaliacao["order_id"].nunique())

print("Repetições completas além da primeira:",
      avaliacao.duplicated().sum())


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


# Mostrar exemplos de notas diferentes
exemplos = avaliacao[
    avaliacao["order_id"].isin(notas_diferentes.head(3).index)
]

print("EXEMPLOS DE PEDIDOS COM NOTAS DIFERENTES:")
print(exemplos.sort_values("order_id").to_string(index=False))
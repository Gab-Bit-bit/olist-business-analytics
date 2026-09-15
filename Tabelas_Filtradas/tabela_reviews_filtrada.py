import pandas as pd

tabela_reviews = pd.read_csv('Tabelas/Tabela_Avaliacao.csv', sep= ';')

tabela_reviews = tabela_reviews[
    [
        'order_id',
        'review_score'
    ]
]

tabela_reviews.to_csv(
    'Tabela_Avaliacao.csv',
    index=False,
    sep=';'
)
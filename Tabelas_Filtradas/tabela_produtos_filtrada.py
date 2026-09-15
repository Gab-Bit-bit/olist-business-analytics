import pandas as pd

tabela_produtos = pd.read_csv('Tabelas/Tabela_Produtos.csv', sep= ';')

tabela_produtos = tabela_produtos[
    [
        'product_id',
        'product_category_name',
        'product_weight_g',
        'product_length_cm',
        'product_height_cm',
        'product_width_cm'
    ]
]

tabela_produtos.to_csv(
    'Tabela_Produtos.csv',
    index=False,
    sep=';'
)
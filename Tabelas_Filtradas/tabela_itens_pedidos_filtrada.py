import pandas as pd

tabela_itens = pd.read_csv('Tabelas/Tabela_Itens.csv', sep= ';')

tabela_itens = tabela_itens[
    [
        'order_id',
        'order_item_id',
        'product_id',
        'seller_id',
        'shipping_limit_date',
        'price',
        'freight_value'
    ]
]

tabela_itens.to_csv(
    'Tabela_Itens.csv',
   index=False,
   sep=';'
)
import pandas as pd

tabela_pedidos = pd.read_csv('Tabelas/Tabela_Pedido.csv', sep= ';')

tabela_pedidos = tabela_pedidos[
    [
        'order_id',
        'customer_id',
        'order_status',
        'order_purchase_timestamp',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
]

tabela_pedidos.to_csv(
    'Tabela_Pedido.csv',
    index= False,
    sep= ';'
)
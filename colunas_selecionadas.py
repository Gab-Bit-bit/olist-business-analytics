import pandas as pd
df = pd.read_csv('Tabelas_Análise_E-commerce/Olist_Order/olist_orders_dataset.csv')

Tabela_Pedido = df[
    [
        'order_id',
        'customer_id',
        'order_status',
        'order_purchase_timestamp',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
]

print(Tabela_Pedido.head(10))

Tabela_Pedido.to_csv(
    'Tabela_Pedido.csv',
    index= False,
    sep= ';'
)

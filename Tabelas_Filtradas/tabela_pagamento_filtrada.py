import pandas as pd

tabela_pagamentos = pd.read_csv('Tabelas/Tabela_Pagamentos.csv', sep= ';')

tabela_pagamentos = tabela_pagamentos[
    [
        'order_id',
        'payment_sequential',
        'payment_type',
        'payment_installments',
        'payment_value'
    ]
]

tabela_pagamentos.to_csv(
    'Tabela_Pagamentos.csv',
    index=False,
    sep=';'
)
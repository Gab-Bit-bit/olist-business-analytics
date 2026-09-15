import pandas as pd

tabela_clientes = pd.read_csv('Tabelas/Tabela_Clientes.csv', sep= ';')
pd.set_option("display.max_columns", 150)

tabela_clientes = tabela_clientes[
    [
        'customer_id',
        'customer_unique_id',
        'customer_city',
        'customer_state',

    ]
]

tabela_clientes.to_csv(
    'Tabela_Clientes.csv',
    index= False,
    sep= ';'
)
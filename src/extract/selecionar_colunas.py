# src/extract/selecionar_colunas.py

import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
INTERIM = Path("data/interim")

# seleção das colunas
TABELAS = {
    "customers": {
        "arquivo": "olist_customers_dataset.csv",
        "colunas": [
            "customer_id",
            "customer_unique_id",
            "customer_city",
            "customer_state"
        ]
    },

    "order_items": {
        "arquivo": "olist_order_items_dataset.csv",
        "colunas": [
            "order_id",
            "order_item_id",
            "product_id",
            "price",
            "freight_value"
        ]
    },

    "order_payments": {
        "arquivo": "olist_order_payments_dataset.csv",
        "colunas": [
            "order_id",
            "payment_sequential",
            "payment_type",
            "payment_installments",
            "payment_value"
        ]
    },

    "order_reviews": {
        "arquivo": "olist_order_reviews_dataset.csv",
        "colunas": [
            "order_id",
            "review_score"
        ]
    },

    "orders": {
        "arquivo": "olist_orders_dataset.csv",
        "colunas": [
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    },

    "products": {
        "arquivo": "olist_products_dataset.csv",
        "colunas": [
            "product_id",
            "product_category_name",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ]
    },
}

def criar_novas_tabelas():

    INTERIM.mkdir(parents=True, exist_ok=True)  # cria a pasta "interim" caso ela ainda não exista

    print("\n")
    for nome, config in TABELAS.items():

        # percorre os .csv da pasta raw
        df = pd.read_csv(
            RAW / config["arquivo"]
        )

        # cria novas tabelas com as colunas selecionadas
        df_filtrado = df[config["colunas"]]

        # salva como .csv na pasta interim
        df_filtrado.to_csv(
            INTERIM / f"{nome}.csv",
            index=False
        )

        print(f"'{nome}.csv'")

    print(f"Tabelas criadas com sucesso!")
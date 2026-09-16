# src/main.py

from extract.download_dataset import download_dataset
from extract.selecionar_colunas import criar_novas_tabelas

download_dataset()
criar_novas_tabelas()
# src/main.py
from extract.download_dataset import download_dataset
from transform.selecionar_colunas import criar_novas_tabelas

def main():
    download_dataset()
    criar_novas_tabelas()

if __name__ == "__main__":
    main()
# src/extract/download_dataset
from config import RAW
import kagglehub    # python3 -m pip install kagglehub pandas

DATASET = "olistbr/brazilian-ecommerce"

# faz download do dataset e carrega na pasta raw
def download_dataset():
    RAW.mkdir(parents=True, exist_ok=True)  # cria a pasta raw caso ela ainda não exista

    kagglehub.dataset_download(
        DATASET,
        output_dir=RAW
    )

    # lista todos os .csv da pasta raw
    arquivos = list(RAW.glob("*.csv"))

    print("\n")
    # mostra os .csv da pasta raw
    for arquivo in arquivos:
        print(f"'{arquivo.name}'")

    print("Dataset baixado com sucesso!")
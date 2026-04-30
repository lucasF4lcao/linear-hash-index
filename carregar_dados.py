import pandas as pd

def carregar_palavras(caminho_arquivo: str) -> pd.DataFrame:
    # le o arquivo como texto puro, sem depender do parser csv
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    # transforma as linhas em um dataframe com uma coluna
    df = pd.DataFrame(linhas, columns=["palavra"])

    # remove espacos e quebras de linha
    df["palavra"] = df["palavra"].fillna("").str.strip()

    # remove linhas vazias
    df = df[df["palavra"] != ""].reset_index(drop=True)

    if df.empty:
        raise ValueError("o arquivo esta vazio ou so contem linhas em branco")

    return df
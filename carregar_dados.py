import pandas as pd

def carregar_palavras(caminho_arquivo: str) -> pd.DataFrame:
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    df = pd.DataFrame(linhas, columns=["palavra"])

    df["palavra"] = df["palavra"].fillna("").str.strip()

    df = df[df["palavra"] != ""].reset_index(drop=True)

    if df.empty:
        raise ValueError("o arquivo esta vazio ou so contem linhas em branco")

    return df
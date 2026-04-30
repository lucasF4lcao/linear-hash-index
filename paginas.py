def calcular_quantidade_paginas(total_registros: int, tamanho_pagina: int) -> int:
    # valida o tamanho da pagina
    if tamanho_pagina <= 0:
        raise ValueError("o tamanho da pagina deve ser maior que zero")

    # faz a divisao arredondando para cima
    return (total_registros + tamanho_pagina - 1) // tamanho_pagina


def adicionar_paginas(df, tamanho_pagina: int):
    # valida o tamanho da pagina
    if tamanho_pagina <= 0:
        raise ValueError("o tamanho da pagina deve ser maior que zero")

    # copia para nao alterar o dataframe original sem querer
    df = df.copy()

    # guarda a posicao de cada registro
    df["indice"] = df.index

    # calcula em qual pagina cada palavra fica
    df["pagina"] = df["indice"] // tamanho_pagina

    return df


# def mostrar_resumo_paginas(df):
#     # pega o numero da primeira e da ultima pagina
#     primeira_pagina = df["pagina"].min()
#     ultima_pagina = df["pagina"].max()

#     print("primeira pagina:")
#     print(df[df["pagina"] == primeira_pagina].head())
#     print()

#     print("ultima pagina:")
#     print(df[df["pagina"] == ultima_pagina].head())
#     print()
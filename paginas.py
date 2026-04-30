def calcular_quantidade_paginas(total_registros: int, tamanho_pagina: int) -> int:
    if tamanho_pagina <= 0:
        raise ValueError("o tamanho da pagina deve ser maior que zero")

    return (total_registros + tamanho_pagina - 1) // tamanho_pagina


def adicionar_paginas(df, tamanho_pagina: int):
    if tamanho_pagina <= 0:
        raise ValueError("o tamanho da pagina deve ser maior que zero")

    df = df.copy()

    df["indice"] = df.index

    df["pagina"] = df["indice"] // tamanho_pagina

    return df
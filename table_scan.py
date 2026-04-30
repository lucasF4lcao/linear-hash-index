def table_scan(df, chave):
    paginas_lidas = 0

    for pagina in sorted(df["pagina"].unique()):
        paginas_lidas += 1

        pagina_df = df[df["pagina"] == pagina]

        # print(f"\npagina {pagina}:")

        for _, linha in pagina_df.iterrows():
            # print("   ", linha["palavra"])

            if linha["palavra"] == chave:
                return {
                    "encontrada": True,
                    "pagina": pagina,
                    "paginas_lidas": paginas_lidas,
                }

    return {"encontrada": False, "pagina": None, "paginas_lidas": paginas_lidas}

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time
import threading
from carregar_dados import carregar_palavras
from paginas import calcular_quantidade_paginas, adicionar_paginas
from table_scan import table_scan
from hash_linear import HashLinear


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SGBD - Comparativo Hash Linear vs Table Scan")
        self.root.geometry("1100x800")

        self.df = None
        self.tabela = None
        self.tempo_indice = 0.0
        self.tempo_scan = 0.0

        self.frame_top = tk.Frame(root, pady=10, bg="#f8f9fa")
        self.frame_top.pack(side=tk.TOP, fill=tk.X)

        tk.Button(
            self.frame_top, text="📁 Abrir TXT", command=self.carregar_arquivo
        ).pack(side=tk.LEFT, padx=5)
        self.label_arquivo = tk.Label(
            self.frame_top, text="Nenhum arquivo", bg="#f8f9fa"
        )
        self.label_arquivo.pack(side=tk.LEFT, padx=5)

        tk.Label(self.frame_top, text="Página:", bg="#f8f9fa").pack(
            side=tk.LEFT, padx=5
        )
        self.entry_pagina = tk.Entry(self.frame_top, width=6)
        self.entry_pagina.insert(0, "100")
        self.entry_pagina.pack(side=tk.LEFT, padx=5)

        self.btn_construir = tk.Button(
            self.frame_top,
            text="⚙️ Construir Índice",
            command=self.iniciar_construcao,
            bg="#0078D7",
            fg="white",
        )
        self.btn_construir.pack(side=tk.LEFT, padx=10)

        self.frame_busca = tk.LabelFrame(
            root, text=" Operações de Busca ", padx=10, pady=10
        )
        self.frame_busca.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(self.frame_busca, text="Palavra:").pack(side=tk.LEFT)
        self.entry_busca = tk.Entry(self.frame_busca, width=30)
        self.entry_busca.pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.frame_busca,
            text="🔎 Busca por ÍNDICE",
            command=self.buscar_indice,
            bg="#28a745",
            fg="white",
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            self.frame_busca,
            text="📑 Busca por SCAN",
            command=self.buscar_scan,
            bg="#6c757d",
            fg="white",
        ).pack(side=tk.LEFT, padx=5)

        self.label_tempos = tk.Label(
            root,
            text="Tempos - Índice: 0.0s | Scan: 0.0s",
            font=("Arial", 10, "bold"),
            fg="#333",
        )
        self.label_tempos.pack(pady=5)

        self.progress_bar = ttk.Progressbar(
            root, orient="horizontal", mode="determinate"
        )
        self.progress_bar.pack(fill=tk.X, padx=10)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        self.frame_log = tk.Frame(self.notebook)
        self.text_output = tk.Text(
            self.frame_log, bg="#1e1e1e", fg="#d4d4d4", font=("Consolas", 10)
        )
        self.text_output.pack(expand=True, fill="both")
        self.notebook.add(self.frame_log, text="📋 Logs e Comparação")

        self.container_visual = tk.Frame(self.notebook)
        self.canvas_v = tk.Canvas(self.container_visual, bg="white")
        self.scrollbar = tk.Scrollbar(
            self.container_visual, orient="vertical", command=self.canvas_v.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas_v, bg="white")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_v.configure(scrollregion=self.canvas_v.bbox("all")),
        )
        self.canvas_v.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_v.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas_v.pack(side="left", expand=True, fill="both")
        self.notebook.add(self.container_visual, text="📂 Visualização")

    def log(self, texto):
        self.text_output.insert(tk.END, texto + "\n")
        self.text_output.see(tk.END)

    def carregar_arquivo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not caminho:
            return

        try:
            if os.path.getsize(caminho) == 0:
                raise ValueError(
                    "O arquivo selecionado está vazio e não pode ser indexado."
                )

            self.df = carregar_palavras(caminho)
            self.label_arquivo.config(text=os.path.basename(caminho), fg="black")
            self.log(f"Sucesso: {len(self.df)} palavras carregadas.")
            self.tabela = None

        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo não encontrado.")
        except ValueError as ve:
            messagebox.showwarning("Arquivo Inválido", str(ve))
        except Exception as e:
            messagebox.showerror(
                "Erro de Leitura", f"Falha ao processar o arquivo:\n{str(e)}"
            )

    def iniciar_construcao(self):
        if self.df is None:
            messagebox.showwarning(
                "Ação Necessária",
                "Carregue um arquivo TXT antes de construir o índice.",
            )
            return

        tam_str = self.entry_pagina.get().strip()
        try:
            tam = int(tam_str)
            if tam <= 0:
                raise ValueError("O número deve ser maior que zero.")

            self.btn_construir.config(state=tk.DISABLED)
            threading.Thread(target=self.worker_index, args=(tam,), daemon=True).start()

        except ValueError:
            messagebox.showerror(
                "Entrada Inválida",
                f"'{tam_str}' não é um tamanho de página válido.\n"
                "Insira um número inteiro positivo (ex: 100).",
            )

    def worker_index(self, tam):
        try:
            inicio_const = time.perf_counter()
            self.df = adicionar_paginas(self.df, tam)
            self.tabela = HashLinear(capacidade_bucket=20)
            paginas_agrupadas = self.df.groupby("pagina")
            self.progress_bar["maximum"] = len(paginas_agrupadas)

            for num_pag, grupo in paginas_agrupadas:

                for _, linha in grupo.iterrows():
                    self.tabela.inserir(linha["palavra"], int(num_pag))

                self.progress_bar["value"] = num_pag

            self.tempo_construcao = time.perf_counter() - inicio_const

            self.root.after(0, self.fim_index)

        except Exception as e:
            self.root.after(
                0, lambda: messagebox.showerror("Erro na Construção", str(e))
            )
            self.root.after(0, lambda: self.btn_construir.config(state=tk.NORMAL))

    def fim_index(self):

        total_registros = len(self.df)

        self.progress_bar["value"] = self.progress_bar["maximum"]
        self.btn_construir.config(state=tk.NORMAL)
        self.log(">>> Índice Construído!")

        taxa_colisao = (self.tabela.colisoes / total_registros) * 100
        taxa_overflow = (self.tabela.overflow / total_registros) * 100

        self.log(">>> ÍNDICE CONSTRUÍDO COM SUCESSO!")
        self.log(f"Tempo de Construção: {self.tempo_construcao:.4f} segundos")
        self.log(
            f"Taxa de Colisões: {taxa_colisao:.2f}% ({self.tabela.colisoes} ocorrências)"
        )
        self.log(
            f"Taxa de Overflow: {taxa_overflow:.2f}% ({self.tabela.overflow} ocorrências)"
        )
        # self.log(f"Configuração Final: Nível {self.tabela.nivel} | Buckets Totais: {len(self.tabela.buckets)}")
        self.log("-" * 40)
        self.atualizar_visualizacao()

    def buscar_indice(self):
        if not self.tabela:
            messagebox.showwarning(
                "Índice Ausente",
                "Você precisa 'Construir o Índice' antes de buscar por ele.",
            )
            return

        chave = self.entry_busca.get().strip()
        if not chave:
            return

        try:
            inicio = time.perf_counter()
            res = self.tabela.buscar(chave)
            self.tempo_indice = time.perf_counter() - inicio

            self.log(
                f"\n[ÍNDICE] Busca: '{chave}' -> {'Achou' if res['encontrada'] else 'Não achou'}"
            )
            self.atualizar_visualizacao(
                destaque_b=res["bucket"], destaque_p=res["pagina"]
            )
            self.log(f"Tempo Gasto: {self.tempo_indice:.8f}s")
            self.comparar_performance()
        except Exception as e:
            self.log(f"Erro na busca por índice: {e}")

    def buscar_scan(self):
        if self.df is None:
            messagebox.showwarning("Dados Ausentes", "Carregue um arquivo primeiro.")
            return

        chave = self.entry_busca.get().strip()
        if not chave:
            return

        try:
            inicio = time.perf_counter()
            res = table_scan(self.df, chave)
            self.tempo_scan = time.perf_counter() - inicio

            self.log(
                f"\n[SCAN] Busca: '{chave}' -> {'Achou' if res['encontrada'] else 'Não achou'}"
            )
            self.atualizar_visualizacao(destaque_p=res.get("pagina"))
            self.log(f"Tempo Gasto: {self.tempo_scan:.8f}s")
            self.comparar_performance()
        except Exception as e:
            self.log(f"Erro no Table Scan: {e}")

    def comparar_performance(self):
        self.label_tempos.config(
            text=f"Tempos - Índice: {self.tempo_indice:.6f}s | Scan: {self.tempo_scan:.6f}s"
        )
        if self.tempo_indice > 0 and self.tempo_scan > 0:
            ganho = self.tempo_scan / self.tempo_indice
            self.log(f"==> O Índice foi {ganho:.2f}x mais rápido que o Table Scan.")

    def atualizar_visualizacao(self, destaque_b=None, destaque_p=None):
        for w in self.scrollable_frame.winfo_children():
            w.destroy()

        if self.df is None:
            return

        tk.Label(
            self.scrollable_frame,
            text="PÁGINAS",
            font=("Arial", 10, "bold"),
            bg="white",
        ).pack()
        f_pags = tk.Frame(self.scrollable_frame, bg="white")
        f_pags.pack()

        exibir_p = {self.df["pagina"].min(), self.df["pagina"].max()}
        if destaque_p is not None:
            exibir_p.add(destaque_p)

        for p_idx in sorted(list(exibir_p)):
            cor = "#FFFACD" if destaque_p == p_idx else "#f0f0f0"
            box = tk.LabelFrame(f_pags, text=f"Pág {p_idx}", bg=cor)
            box.pack(side=tk.LEFT, padx=5, pady=5)

            conteudo = self.df[self.df["pagina"] == p_idx].head(10)["palavra"].tolist()
            txt = "\n".join(conteudo) if conteudo else "(vazia)"
            tk.Label(box, text=txt, bg=cor, font=("Consolas", 9)).pack(padx=5, pady=2)

        tk.Label(
            self.scrollable_frame,
            text="BUCKETS (10 Primeiros + alvo de busca)",
            font=("Arial", 10, "bold"),
            bg="white",
            pady=10,
        ).pack()
        f_buckets = tk.Frame(self.scrollable_frame, bg="white")
        f_buckets.pack()

        indices_buckets = list(range(min(100, len(self.tabela.buckets))))
        if destaque_b is not None and destaque_b >= 10:
            indices_buckets.append(destaque_b)

        for i in indices_buckets:
            if i >= len(self.tabela.buckets):
                continue

            bucket = self.tabela.buckets[i]
            cor = "#90EE90" if destaque_b == i else "white"

            b_box = tk.LabelFrame(f_buckets, text=f"B{i}", bg=cor)
            pos_row = indices_buckets.index(i) // 6
            pos_col = indices_buckets.index(i) % 6
            b_box.grid(row=pos_row, column=pos_col, padx=4, pady=4, sticky="n")

            conteudo = [r["palavra"] for r in bucket[:10]]
            txt_b = "\n".join(conteudo) if conteudo else "(vazio)"
            if len(bucket) > 5:
                txt_b += "\n..."

            tk.Label(b_box, text=txt_b, bg=cor, font=("Consolas", 8), width=12).pack(
                padx=2, pady=2
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

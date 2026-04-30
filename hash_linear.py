class HashLinear:
    def __init__(self, capacidade_bucket=4):
        if capacidade_bucket <= 0:
            raise ValueError("a capacidade do bucket deve ser maior que zero")

        self.capacidade_bucket = capacidade_bucket
        self.nivel = 1
        self.proximo_split = 0
        self.buckets = [[] for _ in range(2)]
        self.total_splits = 0

        self.colisoes = 0
        self.overflow = 0

    def _hash_base(self, chave: str, mod: int) -> int:
        valor = 0
        for caractere in chave:
            valor = (valor * 31 + ord(caractere)) % mod
        return valor

    def calcular_bucket(self, chave: str) -> int:
        bucket = self._hash_base(chave, 2**self.nivel)

        if bucket < self.proximo_split:
            bucket = self._hash_base(chave, 2 ** (self.nivel + 1))

        return bucket

    def inserir(self, palavra: str, pagina: int):
        while True:
            bucket = self.calcular_bucket(palavra)

            registro = {"palavra": palavra, "pagina": pagina}

            # se tá cheio = colisão
            if len(self.buckets[bucket]) >= self.capacidade_bucket:
                self.colisoes += 1

            self.buckets[bucket].append(registro)

            # se passou da capacidade = overflow
            if len(self.buckets[bucket]) <= self.capacidade_bucket:
                break

            # overflow real
            self.overflow += 1

            self.buckets[bucket].pop()
            self._split()

    def _split(self):
        self.buckets.append([])

        bucket_dividido = self.proximo_split
        registros_antigos = self.buckets[bucket_dividido]
        self.buckets[bucket_dividido] = []

        for registro in registros_antigos:
            palavra = registro["palavra"]
            novo_bucket = self._hash_base(palavra, 2 ** (self.nivel + 1))
            self.buckets[novo_bucket].append(registro)

        self.proximo_split += 1
        self.total_splits += 1

        if self.proximo_split == 2**self.nivel:
            self.proximo_split = 0
            self.nivel += 1

    def resumo(self):
        buckets_ocupados = [bucket for bucket in self.buckets if bucket]
        total_buckets = len(self.buckets)
        total_ocupados = len(buckets_ocupados)
        total_registros = sum(len(bucket) for bucket in self.buckets)
        maior_ocupacao = max((len(bucket) for bucket in self.buckets), default=0)
        media_ocupacao = total_registros / total_buckets if total_buckets > 0 else 0

        print("resumo da tabela hash:")
        print("nivel:", self.nivel)
        print("proximo_split:", self.proximo_split)
        print("quantidade total de buckets:", total_buckets)
        print("quantidade de buckets ocupados:", total_ocupados)
        print("total de registros na tabela hash:", total_registros)
        print("maior ocupacao de bucket:", maior_ocupacao)
        print("media de ocupacao por bucket:", round(media_ocupacao, 2))
        print("quantidade de splits realizados:", self.total_splits)
        print()

    def mostrar_buckets(self, limite_buckets=20, limite_por_bucket=5):
        mostrados = 0

        for i, bucket in enumerate(self.buckets):
            if bucket:
                print(f"bucket {i} ({len(bucket)} registros):")

                for registro in bucket[:limite_por_bucket]:
                    print("   ", registro)

                if len(bucket) > limite_por_bucket:
                    print(f"   ... mais {len(bucket) - limite_por_bucket} registros")

                print()
                mostrados += 1

                if mostrados >= limite_buckets:
                    print(
                        f"mostrando apenas os {limite_buckets} primeiros buckets ocupados"
                    )
                    break

    def buscar(self, chave: str):
        bucket = self.calcular_bucket(chave)

        for registro in self.buckets[bucket]:
            if registro["palavra"] == chave:
                return {
                    "encontrada": True,
                    "bucket": bucket,
                    "pagina": registro["pagina"],
                }

        return {"encontrada": False, "bucket": bucket, "pagina": None}

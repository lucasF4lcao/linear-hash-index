# Linear Hashing Simulator

Este projeto é um simulador de motor de busca para **Sistemas de Gerenciamento de Bancos de Dados (SGBD)**. Ele demonstra a eficiência da estrutura de dados **Hashing Linear** em comparação ao método tradicional de varredura completa (**Table Scan**).

O software permite carregar grandes volumes de dados de arquivos de texto, organizá-los em páginas simuladas e construir um índice dinâmico que cresce conforme a necessidade, mantendo a performance de busca otimizada.

## Funcionalidades

- **Indexação Dinâmica:** Implementação de Hashing Linear que ajusta o tamanho da tabela sob demanda.
- **Controle de Overflow:** Gerenciamento de estouro de capacidade de buckets com redistribuição de registros.
- **Paginação de Dados:** Simulação de armazenamento em disco com divisão de registros por blocos/páginas.
- **Análise de Performance:** Comparativo em tempo real entre a busca indexada ($O(1)$ médio) e busca sequencial ($O(n)$).
- **Interface Visual:** GUI desenvolvida em Tkinter com suporte a multithreading para garantir fluidez durante o processamento de dados.

## Conceitos de SGBD Aplicados

### Hashing Linear
Diferente do hashing estático, o Hashing Linear evita o custo proibitivo de reorganizar toda a tabela de uma vez. Através de um **Ponteiro de Split**, a tabela cresce gradualmente, dividindo um bucket por vez sempre que ocorre um overflow em qualquer ponto da estrutura.



### Tratamento de Colisão e Overflow
O projeto monitora e registra estatisticamente:
*   **Colisões:** Quando chaves diferentes apontam para o mesmo bucket.
*   **Overflows:** Quando a capacidade física do bucket é excedida, disparando a expansão da tabela através do ponteiro de split.

## Tecnologias Utilizadas

*   **Python 3.10+**
*   **Pandas:** Para manipulação de dados e simulação de paginação.
*   **Tkinter:** Para a interface gráfica de usuário (GUI).

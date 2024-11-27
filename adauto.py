def imprimir_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print(" ".join("R" if celula else "-" for celula in linha))
    print('\n')


def rainha_da_certo(tabuleiro, linha, coluna, n):
    for i in range(linha):
        if tabuleiro[i][coluna]:
            return False

    for i, j in zip(range(linha, -1, -1), range(coluna, -1, -1)):
        if tabuleiro[i][j]:
            return False

    for i, j in zip(range(linha, -1, -1), range(coluna, n)):
        if tabuleiro[i][j]:
            return False

    return True


def resolver_n_damas(tabuleiro, linha, n, solucoes):
    if linha == n:
        solucoes.append([row[:] for row in tabuleiro])
        return True

    encontrou_solucao = False
    for coluna in range(n):
        if rainha_da_certo(tabuleiro, linha, coluna, n):
            tabuleiro[linha][coluna] = True
            encontrou_solucao = resolver_n_damas(tabuleiro, linha + 1, n, solucoes) or encontrou_solucao
            tabuleiro[linha][coluna] = False

    return encontrou_solucao


def main():
    print('\nProblema das N Damas - AV3 Construção e Análise de Algoritmos\n')

    try:
        numero_damas = int(input("Digite o número de damas no tabuleiro: "))
        if numero_damas < 1:
            print("O número de damas deve ser maior que 0.")
            return

        print(f"\nNúmero de damas escolhido: {numero_damas}\n")

        tabuleiro = [[False for _ in range(numero_damas)] for _ in range(numero_damas)]
        solucoes = []

        resolver_n_damas(tabuleiro, 0, numero_damas, solucoes)

        if solucoes:

            for idx, solucao in enumerate(solucoes, start=1):
                print(f"Solução {idx}:")
                imprimir_tabuleiro(solucao)

            print(f"Número total de soluções: {len(solucoes)}")
        else:
            print("Não existe nenhum caso para este número de damas.")

    except ValueError:
        print("Por favor, insira um número inteiro válido.")

if _name_ == "_main_":
    main()

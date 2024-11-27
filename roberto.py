import csv
import json
from collections import defaultdict, deque

def carregar_dados_creditos(caminho_csv):
    grafo = defaultdict(set)
    nomes_filmes = {}

    with open(caminho_csv, encoding='utf-8') as arquivo:
        reader = csv.DictReader(arquivo)
        for linha in reader:
            filme_id = linha['movie_id']
            nome_filme = linha['title']
            atores = json.loads(linha['cast'])
            nomes_atores = [ator['name'] for ator in atores]

            nomes_filmes[filme_id] = nome_filme
            
            for ator1 in nomes_atores:
                for ator2 in nomes_atores:
                    if ator1 != ator2:
                        grafo[ator1].add((ator2, filme_id))

    return grafo, nomes_filmes


def encontrar_cadeia_atores_bfs(grafo, atorA, atorB):
    if atorA not in grafo or atorB not in grafo:
        return None
    
    visitados = set()
    queue = deque([(atorA, [])])

    while queue:
        ator_atual, caminho = queue.popleft()

        if ator_atual == atorB:
            return caminho
        
        visitados.add(ator_atual)
        for vizinho, filme_id in grafo[ator_atual]:
            if vizinho not in visitados:
                queue.append((vizinho, caminho + [(ator_atual, filme_id, vizinho)]))
    return None

def exibir_cadeia(cadeia, nomes_filmes):
    if not cadeia:
        print("Não há conexão entre os dois atores.")
        return
    print("Cadeia encontrada:")
    for ator1, filme_id, ator2 in cadeia:
        nome_filme = nomes_filmes.get(filme_id, "Desconhecido")
        print(f"{ator1} -> {nome_filme} -> {ator2}")


caminho_csv = "tmdb_5000_credits.csv"

grafo, nomes_filmes = carregar_dados_creditos(caminho_csv)

atorA = input("Digite o nome do ator A: ")
atorB = input("Digite o nome do ator B: ")

cadeia = encontrar_cadeia_atores_bfs(grafo, atorA, atorB)

exibir_cadeia(cadeia, nomes_filmes)

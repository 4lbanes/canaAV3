def maximizar_paginas(capacidade_pendrive, arquivos):
    arquivos.sort(key=lambda x: x[1] / x[2], reverse=True)
    
    selecionados = []
    espaco_usado = 0
    paginas_totais = 0

    for arquivo in arquivos:
        if espaco_usado + arquivo[2] <= capacidade_pendrive:
            selecionados.append(arquivo)
            espaco_usado += arquivo[2]
            paginas_totais += arquivo[1]

    return selecionados, espaco_usado, paginas_totais

if _name_ == "_main_":
    capacidade = int(input("Digite a capacidade do pendrive em MB: "))

    arquivos = [
        ("algoritmos-gulosos.pdf", 150, 30),
        ("merge-sort.pdf", 200, 50),
        ("paradigmas-algoritmos.pdf", 100, 15),
        ("programacao-dinamica.pdf", 180, 25),
        ("metodo-mestre.pdf", 120, 20)
    ]

    selecionados, espaco_usado, paginas_totais = maximizar_paginas(capacidade, arquivos)

    print("\nArquivos selecionados:")
    for pdf in selecionados:
        print(f"- {pdf[0]} (Páginas: {pdf[1]}, Tamanho: {pdf[2]}MB)")

    print(f"\nTotal de páginas: {paginas_totais}")
    print(f"Espaço usado no pendrive: {espaco_usado}MB")

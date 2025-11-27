import sys

def ler_dados(caminho):
    dados = []
    with open(caminho, "r", encoding="utf-8") as arq:
        header = arq.readline().strip()  # SIZE|TOP|QTDE|STATUS
        for linha in arq:
            linha = linha.strip()
            if linha:
                campos = linha.split("|")
                if len(campos) == 6:
                    dados.append({
                        "ano": campos[0],
                        "duracao": campos[1],
                        "titulo": campos[2],
                        "artista": campos[3],
                        "genero": campos[4],
                        "idioma": campos[5],
                        "linha_completa": linha
                    })
    return dados


def ler_consulta(caminho):
    with open(caminho, "r", encoding="utf-8") as arq:
        campo = arq.readline().strip().lower()
        valor = arq.readline().strip()
    return campo, valor


def criar_indice(lista, campo):
    indice = []

    # índice armazena chave + linha completa para facilitar a escrita
    for reg in lista:
        chave = reg[campo]
        indice.append((chave, reg["linha_completa"]))

    # ordenação simples (natural pra um aluno)
    indice = sorted(indice, key=lambda x: x[0])
    return indice


def buscar(indice, valor):
    encontrados = []
    
    for chave, linha in indice:
        if chave == valor:
            encontrados.append(linha)
    
    return encontrados


def escrever_saida(caminho, linhas):
    with open(caminho, "w", encoding="utf-8") as arq:
        if not linhas:
            arq.write("Nenhum resultado encontrado.\n")
        else:
            for l in linhas:
                arq.write(l + "\n")


def main():
    if len(sys.argv) != 4:
        print("Uso incorreto. Exemplo:")
        print("python3 ED2-AT04-IndiceSecundario-MariaEduarda.py musicas.txt entrada.txt saida.txt")
        return

    arq_dados = sys.argv[1]
    arq_entrada = sys.argv[2]
    arq_saida = sys.argv[3]

    dados = ler_dados(arq_dados)
    campo, valor = ler_consulta(arq_entrada)

    campos_validos = ["ano", "duracao", "titulo", "artista", "genero", "idioma"]

    if campo not in campos_validos:
        with open(arq_saida, "w", encoding="utf-8") as arq:
            arq.write("Erro: campo de busca invalido.\n")
        return

    indice = criar_indice(dados, campo)
    resultados = buscar(indice, valor)
    escrever_saida(arq_saida, resultados)


if __name__ == "__main__":
    main()

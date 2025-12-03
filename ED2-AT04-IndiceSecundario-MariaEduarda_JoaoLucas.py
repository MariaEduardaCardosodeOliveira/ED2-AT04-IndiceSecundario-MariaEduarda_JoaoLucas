import sys
import bisect   # Usado para busca binária eficiente no índice ordenado.

class Musica:
    def __init__(self, ano, duracao, titulo, artista, genero, idioma, linha_completa):
        self.ano = ano
        self.duracao = duracao
        self.titulo = titulo
        self.artista = artista
        self.genero = genero
        self.idioma = idioma
        self.linha_completa = linha_completa  # Registro preservado exatamente como no arquivo.

    @staticmethod   # Método estático para criar um objeto Musica a partir de uma linha do arquivo.
    # Divide a linha em campos e valida a quantidade de campos.
    def from_record_line(record_line):
        campos = record_line.split("|")
        if len(campos) != 6:
            raise ValueError("Erro: arquivo de dados invalido.")
        return Musica(*campos, record_line)


def ler_cabecalho(linha_header):
    # Valida o cabeçalho (SIZE, TOP, QTDE, STATUS) conforme padrão da disciplina.
    linha_header = linha_header.strip()
    partes = linha_header.split()

    if len(partes) != 4:
        raise ValueError("Erro: arquivo de dados invalido.")

    info = {}   # Dicionário para armazenar informações do cabeçalho.
    for p in partes:
        if "=" not in p:
            raise ValueError("Erro: arquivo de dados invalido.")
        k, v = p.split("=", 1)
        info[k.upper()] = int(v)

    size = info.get("SIZE")
    top = info.get("TOP")
    qtde = info.get("QTDE")
    status = info.get("STATUS")

    if size != 91 or top != -1 or status != 0 or qtde is None or qtde < 0:
        raise ValueError("Erro: arquivo de dados invalido.")

    return info


def ler_dados(caminho):
    with open(caminho, "r", encoding="utf-8") as arq:
        header_line = arq.readline()
        if not header_line:
            raise ValueError("Erro: arquivo de dados invalido.")

        info = ler_cabecalho(header_line)
        size = info["SIZE"]
        qtde = info["QTDE"]

        musicas = []

        # Lê exatamente QTDE registros, ajustando automaticamente para SIZE caracteres.
        for _ in range(qtde):
            linha = arq.readline()
            if not linha:
                raise ValueError("Erro: arquivo de dados invalido.")

            linha_sem_nl = linha.rstrip("\n")

            # Ajusta automaticamente para o tamanho fixo esperado (SIZE).
            if len(linha_sem_nl) < size:
                # Preenche com espaços à direita.
                linha_sem_nl = linha_sem_nl + " " * (size - len(linha_sem_nl))
            elif len(linha_sem_nl) > size:
                # Trunca para SIZE caracteres.
                linha_sem_nl = linha_sem_nl[:size]

            # Agora a linha está GARANTIDAMENTE com SIZE caracteres.
            musicas.append(Musica.from_record_line(linha_sem_nl))

    return musicas, info



def ler_consulta(caminho):
    with open(caminho, "r", encoding="utf-8") as arq:
        campo = arq.readline()
        if not campo:
            return None, None
        campo = campo.strip().lower()

        valor = arq.readline()
        valor = valor.strip() if valor else ""

    return campo, valor


def criar_indice(musicas, campo):
    # Índice secundário: lista ordenada por chave para permitir busca binária.
    indice = []

    for m in musicas:
        if campo == "ano":
            chave = m.ano
        elif campo == "titulo":
            chave = m.titulo
        elif campo == "artista":
            chave = m.artista
        elif campo == "genero":
            chave = m.genero
        elif campo == "idioma":
            chave = m.idioma
        else:
            continue

        indice.append((chave, m.linha_completa))

    indice.sort(key=lambda x: x[0])
    return indice


def buscar(indice, valor):
    # Busca binária para localizar todas as ocorrências da chave no índice.
    if not indice:
        return []

    chaves = [p[0] for p in indice]
    left = bisect.bisect_left(chaves, valor)
    right = bisect.bisect_right(chaves, valor)

    if left == right:
        return []

    return [indice[i][1] for i in range(left, right)]


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
        print("python3 ED2-AT04.py musicas.txt entrada.txt saida.txt")
        return

    arq_dados = sys.argv[1]
    arq_entrada = sys.argv[2]
    arq_saida = sys.argv[3]

    try:
        musicas, _ = ler_dados(arq_dados)
    except Exception as e:
        with open(arq_saida, "w", encoding="utf-8") as arq:
            arq.write(str(e) + "\n")
        return

    campo, valor = ler_consulta(arq_entrada)

    # Campos válidos segundo o enunciado (duracao não é permitido como busca).
    campos_validos = ["ano", "titulo", "artista", "genero", "idioma"]
    if campo not in campos_validos:
        with open(arq_saida, "w", encoding="utf-8") as arq:
            arq.write("Erro: campo de busca invalido.\n")
        return

    indice = criar_indice(musicas, campo)
    resultados = buscar(indice, valor)
    escrever_saida(arq_saida, resultados)


if __name__ == "__main__":
    main()

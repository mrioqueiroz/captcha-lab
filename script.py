from collections import Counter
from pprint import pprint
from sys import argv
from string import ascii_letters, digits

from PIL import Image, ImageOps
from pytesseract import image_to_string

# Usar como `python script.py nome-da-imagem.png 1.8 1.8 4 8`
# Ou alterar diretamente nas constantes abaixo.
IMAGEM = argv[1]
LIMITE_RUIDOS = float(argv[2])
LIMITE_REFORCO = float(argv[3])
ITERACOES_LIMPEZA = int(argv[4])
ITERACOES_REFORCO = int(argv[5])
NUMERO_DE_CARACTERES = 6
CARACTERES_PERMITIDOS = ascii_letters + digits


def obter_caracteres(imagem):
    caracteres = [list() for _ in range(NUMERO_DE_CARACTERES)]
    resultados = tentar_layouts(imagem)
    for posicao in range(NUMERO_DE_CARACTERES):
        for resultado in resultados:
            for indice, caractere in enumerate(caracteres):
                try:
                    caractere.append(resultado[indice])
                except IndexError:
                    pass
    return caracteres


def tentar_layouts(imagem):
    resultados = []
    layouts = [7, 8, 9, 10, 11, 13]
    for layout in layouts:
        resultados.append(reconhecer_caracteres(imagem, layout))
    return resultados


def reconhecer_caracteres(imagem, layout):
    return image_to_string(
        captcha,
        config=
        f"""--psm {layout}
        -c tessedit_char_whitelist={CARACTERES_PERMITIDOS}""")


def remover_ruidos(imagem):
    largura, altura = imagem.size
    pixels = imagem.load()

    for linha in range(altura):
        for coluna in range(largura):
            if pixels[coluna, linha] > 128:
                continue
            escuros = 0
            for pixel in range(coluna, largura):
                if pixels[pixel, linha] < 128:
                    escuros += 1
                else:
                    break
            if escuros <= LIMITE_RUIDOS:
                for pixel in range(escuros):
                    pixels[coluna + pixel, linha] = 255
            coluna += escuros

    for coluna in range(largura):
        for linha in range(altura):
            if pixels[coluna, linha] > 128:
                continue
            escuros = 0
            for pixel in range(linha, altura):
                if pixels[coluna, pixel] < 128:
                    escuros += 1
                else:
                    break
            if escuros <= LIMITE_RUIDOS:
                for pixel in range(escuros):
                    pixels[coluna, linha + pixel] = 255
            linha += escuros
    return imagem


def reforcar_tracos(imagem):
    largura, altura = imagem.size
    pixels = imagem.load()

    for linha in range(altura):
        for coluna in range(largura):
            if pixels[coluna, linha] < 128:
                continue
            escuros = 0
            for pixel in range(coluna, largura):
                if pixels[pixel, linha] > 128:
                    escuros += 1
                else:
                    break
            if escuros <= LIMITE_REFORCO:
                for pixel in range(escuros):
                    pixels[coluna + pixel, linha] = 0
            coluna += escuros

    for coluna in range(largura):
        for linha in range(altura):
            if pixels[coluna, linha] < 128:
                continue
            escuros = 0
            for pixel in range(linha, altura):
                if pixels[coluna, pixel] > 128:
                    escuros += 1
                else:
                    break
            if escuros <= LIMITE_REFORCO:
                for pixel in range(escuros):
                    pixels[coluna, linha + pixel] = 0
            linha += escuros
    return imagem


def resultado(listas):
    c = [list() for _ in range(6)]
    for i, _ in enumerate(c):
        for lista in listas:
            try:
                c[i].append(lista[i].lower())
            except AttributeError:
                pass
    for i, _ in enumerate(c):
        for lista in listas:
            c[i] = Counter(c[i]).most_common()[0][0]
    for x in c:
        print(f"{x}", end="")


def contar_caracteres(listas):
    for lista in listas:
        mais_comuns = [list() for _ in range(len(listas))]
        for indice, _ in enumerate(mais_comuns):
            try:
                mais_comuns[indice] = Counter(listas[indice]).most_common()[0][0]
            except IndexError:
                pass
    return mais_comuns


if __name__ == "__main__":
    captcha = Image.open(IMAGEM)
    captcha = captcha.convert("1")
    parciais = []
    mais_frequentes = []
    parciais.append(obter_caracteres(captcha))

    for _ in range(ITERACOES_LIMPEZA):
        parciais.append(obter_caracteres(remover_ruidos(captcha)))
    for _ in range(ITERACOES_REFORCO):
        parciais.append(obter_caracteres(reforcar_tracos(captcha)))

    for i in parciais:
        if i not in [" ", "\n"]:
            mais_frequentes.append(contar_caracteres(i))
    resultado(mais_frequentes)

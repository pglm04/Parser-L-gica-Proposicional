# Francisco Ochoa Bonato
# Gabriela Apetz Lima
# Guilherme Augusto Santiago Abib
# Pedro Guimarães Lopes Martins

import sys
from lexer import tokenize
from parser import Parser


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo_de_entrada>")
        return

    caminho_arquivo = sys.argv[1]
    with open(caminho_arquivo, "r") as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip()]

    num_expressoes = int(linhas[0])
    expressoes = linhas[1:]

    if len(expressoes) != num_expressoes:
        print("Número de expressões não corresponde ao informado.")
        return

    for expr in expressoes:
        try:
            tokens = tokenize(expr)
            parser = Parser(tokens)
            valido = parser.parse()
            print("valida" if valido else "inválida")
        except Exception:
            print("inválida")

if __name__ == "__main__":
    main()

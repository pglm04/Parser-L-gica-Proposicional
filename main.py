# Francisco Ochoa Bonato
# Gabriela Apetz Lima
# Guilherme Augusto Santiago Abib
# Pedro Guimarães Lopes Martins
import re
import sys

#####################################################################################
# Parser section

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def accept(self, expected_type):
        if self.current()[0] == expected_type:
            self.pos += 1
            return True
        return False

    def expect(self, expected_type):
        if not self.accept(expected_type):
            raise SyntaxError(f"Esperado {expected_type}, mas encontrado {self.current()}")

    def parse(self):
        try:
            self.formula()
            if self.pos != len(self.tokens):
                raise SyntaxError("Tokens extras após o fim da fórmula")
            return True
        except SyntaxError:
            return False

    def formula(self):
        token_type, value = self.current()

        if token_type == "CONSTANTE":
            self.accept("CONSTANTE")
        elif token_type == "PROPOSICAO":
            self.accept("PROPOSICAO")
        elif self.accept("ABREPAREN"):
            if self.accept("OPERADORUNARIO"):
                self.formula()
                self.expect("FECHAPAREN")
            elif self.accept("OPERADORBINARIO"):
                self.formula()
                self.formula()
                self.expect("FECHAPAREN")
            else:
                raise SyntaxError("Operador esperado após '('")
        else:
            raise SyntaxError("Fórmula inválida")

#####################################################################################
# Lexer section


TOKENS = {
    "ABREPAREN": r"\(",
    "FECHAPAREN": r"\)",
    "OPERADORUNARIO": r"\\neg",
    "OPERADORBINARIO": [r"\\wedge", r"\\vee", r"\\rightarrow", r"\\leftrightarrow"],
    "CONSTANTE": ["true", "false"],
    "PROPOSICAO": r"[0-9][0-9a-z]*"
}

def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i].isspace():
            i += 1
            continue

        match = None

        for token_type, pattern in TOKENS.items():
            if isinstance(pattern, list):
                for subpattern in pattern:
                    regex = re.compile(subpattern)
                    match = regex.match(expr, i)
                    if match:
                        tokens.append((token_type, match.group()))
                        i = match.end()
                        break
                if match:
                    break
            else:
                regex = re.compile(pattern)
                match = regex.match(expr, i)
                if match:
                    tokens.append((token_type, match.group()))
                    i = match.end()
                    break

        if not match:
            raise ValueError(f"Token inválido na posição {i}: {expr[i:]}")

    return tokens

#####################################################################################
# Main section

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

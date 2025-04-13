# Francisco Ochoa Bonato
# Gabriela Apetz Lima
# Guilherme Augusto Santiago Abib
# Pedro Guimarães Lopes Martins

from lexer import tokenize

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

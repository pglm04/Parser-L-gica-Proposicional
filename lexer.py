# Francisco Ochoa Bonato
# Gabriela Apetz Lima
# Guilherme Augusto Santiago Abib
# Pedro Guimarães Lopes Martins

import re

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

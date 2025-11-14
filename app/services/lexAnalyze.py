import re

from app.constants.tokenType import TOKEN_TYPES

regex_parts = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES)
token_regex = re.compile(regex_parts)


def lex_analyze(code):
    """
    Realiza a análise léxica, constrói a tabela de símbolos e coleta erros.
    Retorna uma tupla: (tokens, symbol_table, errors)
    """
    tokens = []
    symbol_table = {}
    errors = []
    line_num = 1  # Linhas iniciam em 1 para melhor feedback ao usuário
    position = 0
    symbol_count = 0

    while position < len(code):
        match = token_regex.match(code, position)

        if not match:
            errors.append(f"Erro Fatal na Posição {position}: Código não tokenizável.")
            break

        token_type = match.lastgroup
        token_value = match.group(token_type)

        # Rastreamento de Linha e Ignorar
        if token_type in ['SKIP', 'COMMENT']:
            line_num += token_value.count('\n')
        elif token_type == 'ERROR':
            errors.append(f"Erro Léxico (Linha {line_num}): Caractere não reconhecido '{token_value}'")
        else:
            # Tratamento de tokens válidos
            if token_type == 'ID':
                if token_value not in symbol_table:
                    symbol_table[token_value] = {
                        'id': symbol_count,
                        'primeira_linha': line_num,
                    }
                    symbol_count += 1

                tokens.append({
                    'tipo': token_type,
                    'valor': token_value,
                    'ref_simbolo': symbol_table[token_value]['id'],
                    'linha': line_num
                })
            else:
                tokens.append({
                    'tipo': token_type,
                    'valor': token_value,
                    'linha': line_num
                })
            # Atualiza o número da linha se o token contiver quebras de linha (ex: strings multi-linha)
            line_num += token_value.count('\n')

        position = match.end()

    return tokens, symbol_table, errors

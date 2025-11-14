TOKEN_TYPES = [
    # Diretiva de pré-processamento
    ('Biblioteca', r'#include\s+(<[^>]+>|"[^"]+")'),
    #('DEFINE', r'#define'),
    ('PreProcessador', r'#\s*(if|ifdef|ifndef|else|elif|endif|undef|pragma|define)\b'),
    # Comentários
    ('Comentário', r'//.*|/\*[\s\S]*?\*/'),

    # Palavras-chave
    ('PalavraChave', r'\b(int|float|char|void|if|else|while|for|return)\b'),
    ('ID', r'[a-zA-Z_à-ÿÀ-ß][a-zA-Z0-9_à-ÿÀ-ß]*'),

    # Literais
    ('NumeroFloat', r'\d+\.\d*([Ee][+-]?\d+)?'),
    ('NumeroInteiro', r'\d+'),
    ('STRING_LITERAL', r'\"([^\\\n]|(\\.))*?\"'),
    ('CHAR_LITERAL', r'\'.\''),

    # Operadores e Pontuadores
    ('MenorIgual', r'<='), ('MaiorIgual', r'>='), ('IgualA', r'=='), ('DiferenteDe', r'!='),
    ('Soma', r'\+'), ('Subtração', r'-'), ('Multiplicação', r'\*'), ('Divisão', r'/'),
    ('Atribuição', r'='), ('MenorQue', r'<'), ('MaiorQue', r'>'),
    ('AbreParentese', r'\('), ('FechaParentese', r'\)'),
    ('AbreColchete', r'\['), ('FechaColchete', r'\]'),
    ('AbreChave', r'{'), ('FechaChave', r'}'),
    ('Vírgula', r','), ('EncerraLinha', r';'),

    # Espaços em branco para ignorar e Erro
    ('SKIP', r'[\s]+'),
    ('ERROR', r'.')
]

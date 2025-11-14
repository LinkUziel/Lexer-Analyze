import tkinter as tk
from tkinter import filedialog, font, scrolledtext, ttk

from app.services.lexAnalyze import lex_analyze


class LexerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analisador Léxico")
        self.geometry("1000x700")

        # Armazena os resultados da última análise
        self.tokens = []
        self.symbol_table = {}
        self.errors = []

        # Estilo
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=5)
        self.style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))

        # Layout principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Painel de Código Fonte
        source_frame = ttk.LabelFrame(main_frame, text="Código Fonte", padding="10")
        source_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.source_code_text = scrolledtext.ScrolledText(source_frame, wrap=tk.WORD, height=10,
                                                          font=("Courier New", 11))
        self.source_code_text.pack(fill=tk.BOTH, expand=True)

        # 2. Frame para os botões de ação
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=5)

        self.load_button = ttk.Button(action_frame, text="Carregar Arquivo C...", command=self.load_file)
        self.load_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.analyze_button = ttk.Button(action_frame, text="Analisar Código", command=self.run_analysis)
        self.analyze_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 5))

        self.save_button = ttk.Button(action_frame, text="Salvar Resultados...", command=self.save_results_to_file,
                                      state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        # 3. Painel de Resultados (dividido)
        results_pane = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        results_pane.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # 3a. Tabela de Símbolos
        symbols_frame = ttk.LabelFrame(results_pane, text="Tabela de Símbolos", padding="5")
        self.symbol_tree = self.create_treeview(symbols_frame, columns=('ID', 'Lexema', 'Linha'))
        results_pane.add(symbols_frame, weight=1)

        # 3b. Lista de Tokens
        tokens_frame = ttk.LabelFrame(results_pane, text="Lista de Tokens", padding="5")
        self.token_tree = self.create_treeview(tokens_frame, columns=('Tipo', 'Ref. T.S.', 'Valor', 'Linha'))
        results_pane.add(tokens_frame, weight=2)

        # 4. Painel de Erros
        errors_frame = ttk.LabelFrame(main_frame, text="Log de Erros", padding="5")
        errors_frame.pack(fill=tk.X, pady=5)
        self.errors_text = scrolledtext.ScrolledText(errors_frame, wrap=tk.WORD, height=4, font=("Courier New", 10),
                                                     state='disabled', background='#f0f0f0')
        self.errors_text.pack(fill=tk.X, expand=True)

    def create_treeview(self, parent, columns):
        """Cria e configura um widget Treeview (tabela)."""
        tree = ttk.Treeview(parent, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.W, width=font.Font().measure(col) * 2)

        # Adiciona scrollbars
        vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        tree.pack(side='left', fill='both', expand=True)

        return tree

    def load_file(self):
        """Abre um diálogo para selecionar e carregar um arquivo .c ou .h."""
        filepath = filedialog.askopenfilename(
            title="Selecionar um arquivo C",
            filetypes=(("Arquivos C", "*.c"), ("Arquivos de Cabeçalho", "*.h"), ("Todos os arquivos", "*.*"))
        )
        if not filepath:
            return

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                code = file.read()
                self.source_code_text.delete('1.0', tk.END)
                self.source_code_text.insert(tk.END, code)
        except Exception as e:
            self.errors_text.config(state='normal')
            self.errors_text.delete('1.0', tk.END)
            self.errors_text.insert(tk.END, f"Erro ao ler o arquivo: {e}")
            self.errors_text.config(state='disabled')

    def run_analysis(self):
        """Executa a análise léxica e atualiza a GUI."""
        code = self.source_code_text.get('1.0', tk.END)
        self.tokens, self.symbol_table, self.errors = lex_analyze(code)

        # Limpa tabelas e logs antigos
        for tree in [self.symbol_tree, self.token_tree]:
            tree.delete(*tree.get_children())

        self.errors_text.config(state='normal')
        self.errors_text.delete('1.0', tk.END)

        # Preenche a Tabela de Símbolos
        sorted_symbols = sorted(self.symbol_table.items(), key=lambda item: item[1]['id'])
        for lexema, info in sorted_symbols:
            self.symbol_tree.insert('', tk.END, values=(info['id'], lexema, info['primeira_linha']))

        # Preenche a Lista de Tokens
        for token in self.tokens:
            ref_ts = token.get('ref_simbolo', '-')
            valor_limpo = repr(token['valor'])[1:-1]  # Usa repr para mostrar escapes como \n
            self.token_tree.insert('', tk.END, values=(token['tipo'], ref_ts, valor_limpo, token['linha']))

        # Exibe os erros
        if self.errors:
            self.errors_text.insert(tk.END, "\n".join(self.errors))
        else:
            self.errors_text.insert(tk.END, "Análise concluída sem erros léxicos.")

        self.errors_text.config(state='disabled')

        # Habilita o botão de salvar se a análise produziu algum resultado
        if self.tokens or self.symbol_table or self.errors:
            self.save_button.config(state=tk.NORMAL)

    def save_results_to_file(self):
        """Salva os resultados da análise em um arquivo de texto."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os arquivos", "*.*")],
            title="Salvar resultados em arquivo"
        )
        if not filepath:
            return

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                # --- Escreve a Tabela de Símbolos ---
                f.write("=" * 50 + "\n")
                f.write("TABELA DE SÍMBOLOS\n")
                f.write("=" * 50 + "\n")
                f.write(f"{'ID':<4} | {'Lexema':<20} | {'Linha'}\n")
                f.write("-" * 50 + "\n")

                simbolos_ordenados = sorted(self.symbol_table.items(), key=lambda item: item[1]['id'])
                for lexema, info in simbolos_ordenados:
                    f.write(f"{info['id']:<4} | {lexema:<20} | {info['primeira_linha']}\n")

                f.write("\n\n")

                # --- Escreve a Lista de Tokens ---
                f.write("=" * 50 + "\n")
                f.write("LISTA DE TOKENS\n")
                f.write("=" * 50 + "\n")
                f.write(f"{'Tipo':<15} | {'Ref. T.S.':<10} | {'Valor':<25} | {'Linha'}\n")
                f.write("-" * 50 + "\n")

                for tok in self.tokens:
                    ref_ts = str(tok.get('ref_simbolo', '-'))
                    valor_limpo = repr(tok['valor'])[1:-1]
                    f.write(f"{tok['tipo']:<15} | {ref_ts:<10} | {valor_limpo:<25} | {tok['linha']}\n")

                f.write("\n\n")

                # --- Escreve o Log de Erros ---
                if self.errors:
                    f.write("=" * 50 + "\n")
                    f.write("LOG DE ERROS\n")
                    f.write("=" * 50 + "\n")
                    for error in self.errors:
                        f.write(error + "\n")
        except Exception as e:
            self.errors_text.config(state='normal')
            self.errors_text.delete('1.0', tk.END)
            self.errors_text.insert(tk.END, f"Erro ao salvar o arquivo: {e}")
            self.errors_text.config(state='disabled')

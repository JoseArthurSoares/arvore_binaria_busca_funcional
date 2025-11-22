from lark import Lark
from transformer import TreeLangTransformer
import json

# 1. Carregar a gramática do arquivo externo
with open('gramatica.lark', 'r') as file:
    grammar_text = file.read()

# 2. Inicializar o Lark
parser = Lark(grammar_text, start='start', parser='lalr', transformer=TreeLangTransformer())

# 3. Função auxiliar para exibir o resultado
def testar(codigo):
    print(f"\n Entrada: {codigo}")
    try:
        resultado = parser.parse(codigo)
        # Pretty print do JSON para facilitar a leitura
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Erro: {e}")

# --- Testes ---
if __name__ == "__main__":
    # Teste 1: Estrutura básica
    testar('Node(10, Empty, Empty)')

    # Teste 2: Insert
    testar('insert(Node(5, Empty, Empty), 8)')

    # Teste 3: Expressão matemática simples
    testar('10 + 20')
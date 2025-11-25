import sys
from lark import Lark
from transformer import LangTransformer, BinOp, UnOp, Let, VarDec, FunDec, IfElse, App, TreeOp, TreeNode, EmptyTree, Var


# --- Lógica de Árvore Binária (Runtime) ---

def _validar_arvore(node, nome_funcao):
    if not isinstance(node, (EmptyTree, TreeNode)):
        raise TypeError(
            f"Erro de Execução em '{nome_funcao}': Esperava uma Árvore, mas recebeu '{type(node).__name__}' ({node}).")


def bst_insert(node, val):
    _validar_arvore(node, "insert")

    if isinstance(node, EmptyTree):
        return TreeNode(val, EmptyTree(), EmptyTree())

    try:
        if val < node.val:
            return TreeNode(node.val, bst_insert(node.left, val), node.right)
        elif val > node.val:
            return TreeNode(node.val, node.left, bst_insert(node.right, val))
        else:
            # Valor duplicado, retorna a mesma árvore
            return TreeNode(node.val, node.left, bst_insert(node.right, val))
    except TypeError:
        raise TypeError(
            f"Erro de Execução: Tipos incompatíveis para comparação. Tentou comparar '{val}' ({type(val).__name__}) com '{node.val}' ({type(node.val).__name__}).")


def bst_search(node, val):
    _validar_arvore(node, "search")

    if isinstance(node, EmptyTree):
        return False

    try:
        if val == node.val:
            return True
        elif val < node.val:
            return bst_search(node.left, val)
        else:
            return bst_search(node.right, val)
    except TypeError:
        raise TypeError(f"Erro de Execução: Tipos incompatíveis na busca. Tentou comparar '{val}' com '{node.val}'.")


def bst_min_value(node):
    current = node
    while not isinstance(current.left, EmptyTree):
        current = current.left
    return current


def bst_remove(node, val):
    _validar_arvore(node, "remove")

    if isinstance(node, EmptyTree):
        return node

    try:
        if val < node.val:
            return TreeNode(node.val, bst_remove(node.left, val), node.right)
        elif val > node.val:
            return TreeNode(node.val, node.left, bst_remove(node.right, val))
        else:
            # Nó encontrado
            if isinstance(node.left, EmptyTree):
                return node.right
            elif isinstance(node.right, EmptyTree):
                return node.left

            # Nó com dois filhos: pega o sucessor in-order
            temp = bst_min_value(node.right)
            return TreeNode(temp.val, node.left, bst_remove(node.right, temp.val))
    except TypeError:
        raise TypeError(f"Erro de Execução: Tipos incompatíveis na remoção.")


def bst_min(node):
    _validar_arvore(node, "min")
    if isinstance(node, EmptyTree):
        raise ValueError("Erro de Execução: Árvore vazia não possui mínimo.")

    while not isinstance(node.left, EmptyTree):
        node = node.left
    return node.val


def bst_max(node):
    _validar_arvore(node, "max")
    if isinstance(node, EmptyTree):
        raise ValueError("Erro de Execução: Árvore vazia não possui máximo.")

    while not isinstance(node.right, EmptyTree):
        node = node.right
    return node.val


def bst_inorder(node):
    _validar_arvore(node, "inorder")
    if isinstance(node, EmptyTree):
        return []

    return bst_inorder(node.left) + [node.val] + bst_inorder(node.right)


# --- Avaliador (Interpreter) ---
def evaluate(node, env):
    if isinstance(node, (int, str, bool, EmptyTree, TreeNode)):
        return node

    if isinstance(node, Var):
        if node.name in env:
            return env[node.name]
        raise ValueError(f"Erro de Variável: '{node.name}' não foi definida.")

    if isinstance(node, str):
        if node in env:
            return env[node]
        raise ValueError(f"Erro de Variável: '{node}' não foi definida.")

    if isinstance(node, BinOp):
        l = evaluate(node.left, env)
        r = evaluate(node.right, env)

        try:
            if node.op == '+': return l + r
            if node.op == '-': return l - r
            if node.op == '++': return str(l) + str(r)
            if node.op == '==': return l == r
            if node.op == 'and': return l and r
            if node.op == 'or': return l or r
        except TypeError:
            raise TypeError(
                f"Erro de Tipo: Operação '{node.op}' inválida entre {l} ({type(l).__name__}) e {r} ({type(r).__name__}).")

    if isinstance(node, UnOp):
        val = evaluate(node.expr, env)
        try:
            if node.op == '-': return -val
            if node.op == 'not': return not val
            if node.op == 'length': return len(str(val))
        except TypeError:
            raise TypeError(f"Erro de Tipo: Operação unária '{node.op}' inválida para o valor {val}.")

    if isinstance(node, TreeOp):
        tree = evaluate(node.tree, env)
        val = evaluate(node.val, env) if node.val is not None else None

        if node.op == 'insert': return bst_insert(tree, val)
        if node.op == 'search': return bst_search(tree, val)
        if node.op == 'remove': return bst_remove(tree, val)
        if node.op == 'min': return bst_min(tree)
        if node.op == 'max': return bst_max(tree)
        if node.op == 'inorder': return bst_inorder(tree)

    if isinstance(node, IfElse):
        cond = evaluate(node.cond, env)
        if not isinstance(cond, bool):
            raise TypeError(f"Erro de Controle: A condição do 'if' deve ser booleana (true/false), recebeu '{cond}'.")

        if cond:
            return evaluate(node.true_branch, env)
        else:
            return evaluate(node.false_branch, env)

    if isinstance(node, Let):
        new_env = env.copy()
        for decl in node.decls:
            if isinstance(decl, VarDec):
                new_env[decl.name] = evaluate(decl.expr, new_env)
            elif isinstance(decl, FunDec):
                new_env[decl.name] = decl
        return evaluate(node.body, new_env)

    if isinstance(node, App):
        func = env.get(node.func_name)
        if not func:
            raise ValueError(f"Erro de Função: '{node.func_name}' não encontrada.")
        if not isinstance(func, FunDec):
            raise ValueError(f"Erro de Tipo: '{node.func_name}' existe, mas não é uma função.")

        if len(func.params) != len(node.args):
            raise ValueError(
                f"Erro de Função: '{node.func_name}' espera {len(func.params)} argumentos, mas recebeu {len(node.args)}.")

        # Cria escopo da função
        func_env = env.copy()
        for param, arg in zip(func.params, node.args):
            func_env[param] = evaluate(arg, env)

        return evaluate(func.body, func_env)

    return node


if __name__ == "__main__":

    def repl():
        try:
            with open("gramatica.lark", "r", encoding='utf-8') as f:
                grammar = f.read()
        except FileNotFoundError:
            print("ERRO CRÍTICO: Arquivo 'gramatica.lark' não encontrado na pasta.")
            return

        parser = Lark(grammar, parser='lalr', transformer=LangTransformer())
        print("LF1 REPL (Modo Seguro) — digite 'exit' ou Ctrl+C para sair")

        while True:
            try:
                text = input("expr> ").strip()
                if text == "":
                    continue
                if text.lower() in ("exit", "quit"):
                    break

                ast_node = parser.parse(text)
                # print("AST DEBUG:", ast_node)
                result = evaluate(ast_node, {})
                print(f"=> {result}")

            except KeyboardInterrupt:
                print("\nSaindo.")
                break
            except Exception as e:
                print(f"{e}")


    if __name__ == "__main__":
        repl()
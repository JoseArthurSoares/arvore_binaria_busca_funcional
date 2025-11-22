import sys
from lark import Lark
from transformer import LangTransformer, BinOp, UnOp, Let, VarDec, FunDec, IfElse, App, TreeOp, TreeNode, EmptyTree, Var


# --- Lógica de Árvore Binária (Runtime) ---
def bst_insert(node, val):
    if isinstance(node, EmptyTree):
        return TreeNode(val, EmptyTree(), EmptyTree())

    if val < node.val:
        return TreeNode(node.val, bst_insert(node.left, val), node.right)
    elif val > node.val:
        return TreeNode(node.val, node.left, bst_insert(node.right, val))
    else:
        return node  # Valor duplicado, retorna a mesma árvore


def bst_search(node, val):
    if isinstance(node, EmptyTree):
        return False
    if val == node.val:
        return True
    elif val < node.val:
        return bst_search(node.left, val)
    else:
        return bst_search(node.right, val)


def bst_min_value(node):
    current = node
    while not isinstance(current.left, EmptyTree):
        current = current.left
    return current


def bst_remove(node, val):
    if isinstance(node, EmptyTree):
        return node

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


# --- Avaliador (Interpreter) ---
def evaluate(node, env):
    if isinstance(node, int) or isinstance(node, str) or isinstance(node, bool):
        return node
    if isinstance(node, EmptyTree) or isinstance(node, TreeNode):
        return node

    if isinstance(node, Var):
        if node.name in env:
            return env[node.name]
        raise ValueError(f"Variável não definida: {node.name}")

    if isinstance(node, str):  # Variável
        if node in env:
            return env[node]
        raise ValueError(f"Variável não definida: {node}")

    if isinstance(node, BinOp):
        l = evaluate(node.left, env)
        r = evaluate(node.right, env)
        if node.op == '+': return l + r
        if node.op == '-': return l - r
        if node.op == '++': return str(l) + str(r)
        if node.op == '==': return l == r
        if node.op == 'and': return l and r
        if node.op == 'or': return l or r

    if isinstance(node, UnOp):
        val = evaluate(node.expr, env)
        if node.op == '-': return -val
        if node.op == 'not': return not val
        if node.op == 'length': return len(str(val))

    if isinstance(node, TreeOp):
        tree = evaluate(node.tree, env)
        val = evaluate(node.val, env)

        if node.op == 'insert': return bst_insert(tree, val)
        if node.op == 'search': return bst_search(tree, val)
        if node.op == 'remove': return bst_remove(tree, val)

    if isinstance(node, IfElse):
        cond = evaluate(node.cond, env)
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
        if not func or not isinstance(func, FunDec):
            raise ValueError(f"Função não encontrada: {node.func_name}")

        # Cria escopo da função
        func_env = env.copy()
        for param, arg in zip(func.params, node.args):
            func_env[param] = evaluate(arg, env)

        return evaluate(func.body, func_env)

    return node


# --- Execução Principal ---
def main():
    # Lê a gramática
    with open("gramatica.lark", "r") as f:
        grammar = f.read()

    parser = Lark(grammar, parser='lalr', transformer=LangTransformer())

    codigo = """
    let 
        var x = 10,
        var y = 20
    in
        x + y
    """

    print(f"Código fonte:\n{codigo}\n")

    try:
        tree = parser.parse(codigo)
        resultado = evaluate(tree, {})
        print(f"Resultado da execução: {resultado}")


    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
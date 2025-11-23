from lark import Transformer, v_args
from dataclasses import dataclass
from typing import List, Any

@dataclass
class Var:
    name: str

# --- Definição dos Nós da AST ---
@dataclass
class BinOp:
    left: Any
    op: str
    right: Any


@dataclass
class UnOp:
    op: str
    expr: Any


@dataclass
class Let:
    decls: List[Any]
    body: Any


@dataclass
class VarDec:
    name: str
    expr: Any


@dataclass
class FunDec:
    name: str
    params: List[str]
    body: Any


@dataclass
class IfElse:
    cond: Any
    true_branch: Any
    false_branch: Any


@dataclass
class App:
    func_name: str
    args: List[Any]


@dataclass
class TreeOp:
    op: str
    tree: Any
    val: Any


@dataclass
class TreeNode:
    val: Any
    left: Any
    right: Any


class EmptyTree:
    def __repr__(self): return "Empty"


# --- Transformer ---
@v_args(inline=True)
class LangTransformer(Transformer):
    def val_int(self, n): return int(n)

    def val_string(self, s): return s[1:-1]  # Remove as aspas

    def val_bool_true(self): return True

    def val_bool_false(self): return False

    def id(self, name): return Var(str(name))

    # Árvores Concretas
    def val_empty(self): return EmptyTree()

    def val_node(self, val, left, right): return TreeNode(val, left, right)

    # Operações Binárias
    def bin_add(self, l, r): return BinOp(l, '+', r)

    def bin_sub(self, l, r): return BinOp(l, '-', r)

    def bin_concat(self, l, r): return BinOp(l, '++', r)

    def bin_eq(self, l, r): return BinOp(l, '==', r)

    def bin_and(self, l, r): return BinOp(l, 'and', r)

    def bin_or(self, l, r): return BinOp(l, 'or', r)

    # Operações Unárias
    def un_neg(self, e): return UnOp('-', e)

    def un_not(self, e): return UnOp('not', e)

    def un_len(self, e): return UnOp('length', e)

    # Operações de Árvore
    def tree_insert(self, tree, val): return TreeOp('insert', tree, val)

    def tree_remove(self, tree, val): return TreeOp('remove', tree, val)

    def tree_search(self, tree, val): return TreeOp('search', tree, val)

    # Controle de Fluxo
    def if_then_else(self, c, t, e): return IfElse(c, t, e)

    # Declarações e Funções
    def exp_declaracao(self, decls, body): return Let(decls, body)

    def dec_variavel(self, var_node, expr):
        return [VarDec(var_node.name, expr)]

    def dec_funcao(self, var_node, params, body):
        param_names = [p.name for p in params]
        return [FunDec(var_node.name, param_names, body)]

    def dec_composta(self, d1, d2): return d1 + d2

    def list_id(self, *args): return list(args)

    def aplicacao(self, var_node, args):
        return App(var_node.name, args)

    def list_exp(self, *args): return list(args)

    def tree_min(self, tree): 
        return TreeOp('min', tree, None)

    def tree_max(self, tree): 
        return TreeOp('max', tree, None)

    def tree_inorder(self, tree):
        return TreeOp('inorder', tree, None)
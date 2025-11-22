from lark import Transformer


class TreeLangTransformer(Transformer):
    def valor_inteiro(self, items):
        return int(items[0])

    def valor_string(self, items):
        return str(items[0][1:-1])

    def valor_booleano(self, items):
        return items[0] == "true"

    def valor_lista(self, items):
        return list(items)

    # --- Árvore ---
    def empty_tree(self, items):
        return None

    def node_tree(self, items):
        valor, esq, dir = items
        return {"tipo": "Node", "valor": valor, "left": esq, "right": dir}

    # --- Operações ---
    def insert_tree(self, items):
        arvore, valor = items
        return {"op": "insert", "target": arvore, "value": valor}

    def remove_tree(self, items):
        arvore, valor = items
        return {"op": "remove", "target": arvore, "value": valor}

    def search_tree(self, items):
        arvore, valor = items
        return {"op": "search", "target": arvore, "value": valor}

    # --- Outros ---
    def id(self, items):
        return str(items[0])

    def add(self, items):
        return items[0] + items[1]
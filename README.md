# Árvore Binária de Busca Funcional

## Disciplina

(IN1007) Paradigmas de Linguagens de Programação - CIn/UFPE

## Professor

Augusto Sampaio

## Equipe

* José Arthur Soares Bezerra | jasb@cin.ufpe.br
* Tiago Regis Perrelli | trp@cin.ufpe.br
* Ricardo Helisson Bezerra Amorim | rhba@cin.ufpe.br

## Contextualização

Este projeto foca na implementação de uma estrutura de dados clássica, a Árvore Binária de Busca (BST), sob a ótica do paradigma da linguagem funcional 3. A implementação visa não apenas replicar as operações básicas de inserção e busca, mas garantir que todas as modificações na estrutura preservem a **imutabilidade**. O conceito central explorado será o de **compartilhamento estrutural** (*structural sharing*), também conhecido como *path copying*, que permite a criação eficiente de novas versões da árvore a cada operação, sem alterar a original.

## Escopo do Projeto

O objetivo é desenvolver um tipo `Árvore` polimórfico que permita armazenar e manipular dados ordenados. A funcionalidade central é a implementação das operações de `inserir`, `remover` e `buscar` de forma puramente funcional, onde qualquer operação de escrita deve retornar uma nova instância da árvore com a modificação aplicada, mantendo a versão anterior intacta e acessível.

## Gramática BNF

A gramática a seguir representa a Linguagem Funcional 3 estendida com definições para a estrutura de dados Árvore Binária de Busca e suas operações:

```
# Novo tipo de dado "ValorArvore"
ValorConcreto ::= ValorInteiro
                | ValorBooleano
                | ValorString
                | ValorLista
                | ValorArvore


# Esse novo tipo de dado representa uma árvore binária. "Empty" representa uma árvore vazia, enquanto "Node" representa um nó da árvore com três componentes: o valor armazenado no nó, a subárvore esquerda e a subárvore direita.
ValorArvore ::= "Empty"
              | "Node" "(" Expressao "," Expressao "," Expressao ")"


# Nova expressão "ExpArvore" para manipulação de árvores binárias
Expressao ::= Valor
            | ExpUnaria
            | ExpBinaria ::= Expressao "+" Expressao
             | Expressao "-" Expressao
             | Expressao "*" Expressao
             | Expressao "/" Expressao
             | Expressao "==" Expressao
             | Expressao "<" Expressao
             | Expressao ">" Expressao
             | Expressao "<=" Expressao
             | Expressao ">=" Expressao
             | Expressao "and" Expressao
             | Expressao "or" Expressao
            | ExpDeclaracao
            | Id
            | Aplicacao
            | IfThenElse
            | ExpArvore

# Operações de inserção, remoção e busca em árvores binárias são definidas pela expressão "ExpArvore". Cada operação recebe dois argumentos: a árvore alvo e o valor a ser inserido, removido ou buscado.
ExpArvore ::= "insert" "(" Expressao "," Expressao ")" 
            | "remove" "(" Expressao "," Expressao ")" 
            | "search" "(" Expressao "," Expressao ")"

```
## Exemplos de Uso
### Exemplo 1 - Inserção inicial na árvore
Expressão formal
```
insert(Empty, 5)
```
Descrição:

A expressão insert(Empty, 5) insere o valor 5 em uma árvore vazia (Empty).
O resultado é um novo ValorArvore contendo um único nó com valor 5.

Visualização estrutural
```
  5
 / \
∅   ∅
```
Resultado

O valor retornado é uma nova árvore contendo apenas o nó raiz:
```
Node(5, Empty, Empty)
```
### Exemplo 2 - Construção incremental de uma árvore
Expressão formal
```
let var a1 = insert(Empty, 8) in
let var a2 = insert(a1, 3) in
let var a3 = insert(a2, 10) in
a3
```
Descrição:

Neste exemplo, são realizadas três inserções sucessivas: 

1. Criação da árvore com o valor 8;
2. Inserção de 3 (menor que 8, vai para a esquerda);
3. Inserção de 10 (maior que 8, vai para a direita).

Cada operação insert é uma expressão ExpArvore que gera uma nova instância da árvore, sem modificar as anteriores (imutabilidade).

Visualização estrutural final
```
       8
      / \
     3   10
    / \  / \
   ∅  ∅ ∅  ∅
```
Resultado
```
Node(8, Node(3, Empty, Empty), Node(10, Empty, Empty))
```
### Exemplo 3 - Busca de elemento na árvore (search)
Expressão formal
```
let var arv1 = insert(Empty, 8) in
let var arv2 = insert(arv1, 3) in
let var arv3 = insert(arv2, 10) in
search(arv3, 10)
```
Descrição:

A expressão search(arv3, 10) percorre a árvore para verificar se o valor 10 está presente.
O processo ocorre de forma recursiva:

1. Compara o valor buscado com o valor da raiz (8);
2. Como 10 > 8, desce pela subárvore direita;
3. Encontra o nó 10 → retorna true.

Visualização estrutural da árvore pesquisada
```
       8
      / \
     3   10
    / \  / \
   ∅  ∅ ∅  ∅
```
Resultado da avaliação
```
true
```
Caso alternativo:

Se a busca fosse search(arv3, 5), o percurso terminaria em Empty, retornando:
```
false
```
### Exemplo 4 - Remoção de elemento (remove)
Expressão formal
```
let var t0 = Empty in
let var t1 = insert(t0, 20) in
let var t2 = insert(t1, 10) in
let var t3 = insert(t2, 30) in
let var t4 = insert(t3, 25) in
remove(t4, 20)
```
Descrição:

Neste exemplo, o valor 20 (raiz) é removido da árvore.
O nó é substituído pelo sucessor in-order (menor valor da subárvore direita, que é 25).
A operação cria uma nova versão da árvore, preservando a original.

Estrutura antes da remoção
```
        20
       /  \
     10    30
           /
         25
```
Estrutura após a remoção
```
        25
       /  \
     10    30
```
Resultado
```
Node(25, Node(10, Empty, Empty), Node(30, Empty, Empty))
```

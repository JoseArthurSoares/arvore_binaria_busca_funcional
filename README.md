# Árvore Binária de Busca Funcional

## Disciplina

(IN1007) Paradigmas de Linguagens de Programação - CIn/UFPE

## Professor

Augusto Sampaio

## Equipe

* José Arthur Soares Bezerra | jasb@cin.ufpe.br
* Tiago Regis Perrelli | trp@cin.ufpe.br

## Contextualização

Este projeto foca na implementação de uma estrutura de dados clássica, a Árvore Binária de Busca (BST), sob a ótica do paradigma da linguagem funcional 3. A implementação visa não apenas replicar as operações básicas de inserção e busca, mas garantir que todas as modificações na estrutura preservem a **imutabilidade**. O conceito central explorado será o de **compartilhamento estrutural** (*structural sharing*), também conhecido como *path copying*, que permite a criação eficiente de novas versões da árvore a cada operação, sem alterar a original.

## Escopo do Projeto

O objetivo é desenvolver um tipo `Árvore` polimórfico que permita armazenar e manipular dados ordenados. A funcionalidade central é a implementação das operações de `inserir`, `remover` e `buscar` de forma puramente funcional, onde qualquer operação de escrita deve retornar uma nova instância da árvore com a modificação aplicada, mantendo a versão anterior intacta e acessível.

## Gramática BNF

A gramática a seguir representa a Linguagem de Expressões 3 estendida com definições para a estrutura de dados Árvore Binária de Busca e suas operações:

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
            | ExpBinaria
            | ExpDeclaracao
            | Id
            | Aplicacao
            | IfThenElse
            | ExpArvore

# Operações de inserção, remoção e busca em árvores binárias são definidas pela expressão "ExpArvore". Cada operação recebe dois argumentos: a árvore alvo e o valor a ser inserido, removido ou buscado.
ExpArvore ::= "insert" "(" Expressao "," Expressao ")" 
            | "remove" "(" Expressao "," Expressao ")" 
            | "search" "(" Expressao "," Expressao ")"

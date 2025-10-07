# Árvore Binária de Busca Funcional

## Disciplina

(IN1007) Paradigmas de Linguagens de Programação - CIn/UFPE

## Professor

Augusto Sampaio

## Equipe

* José Arthur Soares Bezerra | jasb@cin.ufpe.br

## Contextualização

Este projeto foca na implementação de uma estrutura de dados clássica, a Árvore Binária de Busca (BST), sob a ótica de um paradigma puramente funcional. A implementação visa não apenas replicar as operações básicas de inserção e busca, mas garantir que todas as modificações na estrutura preservem a **imutabilidade**. O conceito central explorado será o de **compartilhamento estrutural** (*structural sharing*), também conhecido como *path copying*, que permite a criação eficiente de novas versões da árvore a cada operação, sem alterar a original.

## Escopo do Projeto

O objetivo é desenvolver um tipo `Árvore` polimórfico que permita armazenar e manipular dados ordenados. A funcionalidade central é a implementação das operações de `inserir`, `remover` e `buscar` de forma puramente funcional, onde qualquer operação de escrita deve retornar uma nova instância da árvore com a modificação aplicada, mantendo a versão anterior intacta e acessível.

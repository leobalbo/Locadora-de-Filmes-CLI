# Locadora de Filmes CLI - Sistema de Gerenciamento

Este projeto implementa um sistema de gerenciamento para uma locadora de filmes através de uma Interface de Linha de Comando (CLI - Command Line Interface). Ele permite cadastrar filmes e clientes, além de controlar as operações de aluguel e devolução.

---

## Integrantes do Projeto

* **Leonardo:** (RA: 2009203)
* **Carlos:** (RA: 1988692)
* **George:** (RA: 2012100)

---

## Requisitos de Execução

Para executar este sistema, você precisará ter o **Python 3.12** ou superior instalado no seu computador. Nenhuma biblioteca externa adicional é necessária, pois o projeto utiliza apenas módulos padrão do Python e um módulo local para a lista duplamente encadeada.

**Como Executar:**

1.  Navegue até o diretório raiz do projeto pelo seu terminal.
2.  Execute o arquivo principal `main.py` usando o comando:
    ```bash
    python main.py
    ```
3.  O sistema iniciará. Siga as opções do menu para utilizar o sistema.

---

## O Que e Como o Sistema Faz

O sistema oferece uma interface baseada em texto para gerenciar as operações de uma locadora de filmes. As principais funcionalidades são:

### Gerenciamento de Filmes

* **Adicionar Novo Filme:** Permite inserir novos filmes no catálogo, solicitando Título, Ano, Diretor, Gêneros (separados por vírgula) e Atores (separados por vírgula). Cada filme recebe um ID único.
* **Listar Todos os Filmes:** Exibe todos os filmes presentes no catálogo, incluindo seus detalhes e status (disponível ou alugado).
* **Listar Filmes Disponíveis:** Mostra apenas os filmes que estão atualmente disponíveis para aluguel.
* **Listar Filmes Alugados:** Mostra os filmes que estão alugados, indicando quem os alugou e a data do aluguel.
* **Buscar Filme por ID:** Permite encontrar um filme específico fornecendo seu ID.
* **Remover Filme:** Remove um filme do catálogo pelo seu ID, mas apenas se ele não estiver alugado.

### Gerenciamento de Clientes

* **Adicionar Novo Cliente:** Cadastra novos clientes, solicitando Nome e Contato. Cada cliente recebe um ID único.
* **Listar Todos os Clientes:** Exibe a lista de todos os clientes cadastrados, com seus IDs e contatos.
* **Ver Histórico de Aluguéis:** Mostra o histórico completo de aluguéis de um cliente específico, incluindo filmes alugados e devolvidos.

### Operações de Aluguel

* **Alugar Filme:** Realiza a operação de aluguel, associando um filme (pelo ID) a um cliente (pelo ID) e atualizando o status do filme.
* **Devolver Filme:** Realiza a devolução de um filme (pelo ID), atualizando seu status para 'disponível' e registrando a data de devolução no histórico do cliente.

---

## Justificativa da Escolha das Estruturas de Dados

A seleção das estruturas de dados foi pensada para otimizar as operações do sistema:

1.  **`DoublyLinkedList` (Lista Duplamente Encadeada):**
    * **Uso:** Catálogo principal de filmes (`catalogo_filmes_dll`).
    * **Justificativa:** Permite inserções e remoções eficientes (O(1) se o nó é conhecido), facilitando a gestão do catálogo, mesmo que a busca linear seja O(n).

2.  **`dict` (Dicionário):**
    * **Uso:** Mapeamento de IDs para nós (`filmes_por_id_idx`), armazenamento de clientes (`clientes_cadastrados`), índices (`generos_para_filmes_idx`, etc.).
    * **Justificativa:** Oferece acesso, inserção e remoção em tempo médio O(1), ideal para buscas rápidas por ID e para criar índices eficientes.

3.  **`set` (Conjunto):**
    * **Uso:** Gêneros dos filmes e IDs nos índices.
    * **Justificativa:** Garante a unicidade dos elementos (sem gêneros repetidos) e operações rápidas (O(1)) de adição, remoção e verificação de pertencimento.

4.  **`list` (Lista):**
    * **Uso:** Atores dos filmes, histórico de aluguéis (`historico_alugueis`) e histórico de comandos (`historico_comandos_menu`).
    * **Justificativa:** Coleção ordenada e mutável, adequada para sequências onde a ordem pode ser relevante ou para agrupar múltiplos itens. Permite o uso como **Pilha** (com `append` e `pop` ou acesso pelo final, como no `historico_comandos_menu`) ou **Fila** (com `append` e `pop(0)`).

5.  **`tuple` (Tupla):**
    * **Uso:** Armazenamento dos registros individuais dentro do `historico_alugueis` de cada cliente, no formato `(id_filme, titulo, data_aluguel, data_devolucao)`.
    * **Justificativa:** Tuplas são **imutáveis**. Usá-las para registros de histórico é uma boa prática, pois garante que um registro, uma vez criado e finalizado, não seja alterado acidentalmente. Isso traz mais integridade aos dados históricos do sistema. Embora exija a substituição da tupla inteira para registrar a devolução, isso reforça a ideia de que um "evento" de aluguel foi concluído e um novo estado (com data de devolução) foi registrado.

def exibir_menu_principal():
    print("\n=========== LOCADORA DE FILMES CLI ===========")
    print("--- Gerenciar Filmes ---")
    print("1. Adicionar novo filme ao catálogo")
    print("2. Listar todos os filmes do catálogo")
    print("3. Listar filmes disponíveis")
    print("4. Listar filmes alugados")
    print("5. Buscar filme por ID")
    print("6. Remover filme do catálogo (por ID)")
    print("--- Gerenciar Clientes ---")
    print("10. Adicionar novo cliente")
    print("11. Listar todos os clientes")
    print("12. Ver histórico de aluguéis de um cliente")
    print("--- Operações de Aluguel ---")
    print("20. Alugar filme")
    print("21. Devolver filme")
    print("0. Sair do programa")
    print("===============================================")

def obter_escolha_usuario() -> int:
    while True:
        try:
            escolha = int(input("Digite sua opção: "))
            return escolha
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

def obter_detalhes_filme_usuario() -> dict | None:
    print("\n--- Adicionar Novo Filme ao Catálogo ---")
    titulo = input("Título do filme: ").strip()
    if not titulo: print("O título é obrigatório."); return None
    try:
        ano = int(input("Ano de lançamento: "))
    except ValueError: print("Ano inválido."); return None
    diretor = input("Diretor: ").strip()
    generos_str = input("Gêneros (separados por vírgula): ").strip()
    generos = set(g.strip().capitalize() for g in generos_str.split(',') if g.strip()) if generos_str else set()
    atores_str = input("Atores principais (separados por vírgula): ").strip()
    atores = [a.strip() for a in atores_str.split(',') if a.strip()] if atores_str else []
    return {"titulo": titulo, "ano": ano, "diretor": diretor, "generos": generos, "atores": atores}

def obter_detalhes_cliente_usuario() -> dict | None:
    print("\n--- Adicionar Novo Cliente ---")
    nome = input("Nome do cliente: ").strip()
    if not nome: print("Nome é obrigatório."); return None
    contato = input("Contato (telefone/email): ").strip()
    return {"nome": nome, "contato": contato}

def iniciar_interface(gerenciador):
    historico_comandos_menu = [] 
    while True:
        exibir_menu_principal()
        escolha = obter_escolha_usuario()
        historico_comandos_menu.append(escolha)

        if escolha == 1:
            detalhes = obter_detalhes_filme_usuario()
            if detalhes:
                gerenciador.adicionar_filme_catalogo(
                    detalhes["titulo"], detalhes["ano"], detalhes["diretor"],
                    detalhes["generos"], detalhes["atores"]
                )
        elif escolha == 2:
            gerenciador.listar_todos_os_filmes()
        elif escolha == 3:
            gerenciador.listar_filmes_por_status('disponivel')
        elif escolha == 4:
            gerenciador.listar_filmes_por_status('alugado')
        elif escolha == 5:
            id_filme = input("Digite o ID do filme para buscar: ").strip()
            filme = gerenciador.buscar_filme_por_id(id_filme)
            if filme:
                print(f"\nDetalhes: {filme['titulo']} ({filme['ano']}), Status: {filme['status']}")
                if filme['status'] == 'alugado':
                    cliente_alugou = gerenciador.buscar_cliente_por_id(filme.get('id_cliente_alugou', ''))
                    nome_cliente = cliente_alugou['nome'] if cliente_alugou else "Desconhecido"
                    print(f"Alugado por: {nome_cliente} (ID Cliente: {filme.get('id_cliente_alugou', 'N/A')}) em {filme.get('data_aluguel', 'N/A')}")
        elif escolha == 6:
            id_filme = input("Digite o ID do filme para remover do catálogo: ").strip()
            gerenciador.remover_filme_catalogo(id_filme)
        elif escolha == 10:
            detalhes_cliente = obter_detalhes_cliente_usuario()
            if detalhes_cliente:
                gerenciador.adicionar_cliente(detalhes_cliente['nome'], detalhes_cliente['contato'])
        elif escolha == 11:
            gerenciador.listar_clientes()
        elif escolha == 12:
            id_cliente = input("Digite o ID do cliente para ver o histórico: ").strip()
            gerenciador.ver_historico_cliente(id_cliente)
        elif escolha == 20:
            id_filme = input("Digite o ID do filme a ser alugado: ").strip()
            id_cliente = input("Digite o ID do cliente que está alugando: ").strip()
            gerenciador.alugar_filme(id_filme, id_cliente)
        elif escolha == 21:
            id_filme = input("Digite o ID do filme a ser devolvido: ").strip()
            gerenciador.devolver_filme(id_filme)
        elif escolha == 0:
            print("\nObrigado por usar a Locadora de Filmes CLI!")
            if len(historico_comandos_menu) > 1:
                print("Últimas opções de menu selecionadas (da mais recente para a mais antiga):")
                for cmd in reversed(historico_comandos_menu[-6:-1]): 
                    print(f" -> Opção {cmd}")
            break
        else:
            print("Opção desconhecida. Por favor, tente novamente.")
        if escolha != 0:
            input("\nPressione Enter para continuar...")
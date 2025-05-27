import uuid
import datetime
from linkedlist import DoublyLinkedList, Node

def gerar_id_unico():
    return str(uuid.uuid4().hex)[:4]

def criar_payload_filme(titulo: str, ano: int, diretor: str, generos: set, atores: list) -> dict:
    if not isinstance(titulo, str) or not titulo.strip():
        raise ValueError("O título do filme não pode ser vazio.")
    if not isinstance(ano, int) or not (1820 < ano < 2050):
        raise ValueError("Ano de lançamento inválido.")
    if not isinstance(diretor, str) or not diretor.strip():
        diretor = "Desconhecido"
    if not isinstance(generos, set): generos = set(generos)
    if not isinstance(atores, list): atores = list(atores)
    return {
        'id': gerar_id_unico(), 'titulo': titulo, 'ano': ano, 'diretor': diretor,
        'generos': generos, 'atores': atores, 'status': 'disponivel',
        'id_cliente_alugou': None, 'data_aluguel': None
    }

def criar_payload_cliente(nome: str, contato: str) -> dict:
    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("O nome do cliente não pode ser vazio.")
    return {
        'id_cliente': "cliente_" + gerar_id_unico(), 'nome': nome,
        'contato': contato, 'historico_alugueis': []
    }

class GerenciadorLocadora:
    def __init__(self):
        self.catalogo_filmes_dll = DoublyLinkedList()
        self.filmes_por_id_idx = {}
        self.generos_para_filmes_idx = {}
        self.atores_para_filmes_idx = {}
        self.diretores_para_filmes_idx = {}
        self.clientes_cadastrados = {}

    def _adicionar_filme_aos_indices(self, dados_filme: dict):
        id_filme = dados_filme['id']
        for genero in dados_filme.get('generos', set()):
            self.generos_para_filmes_idx.setdefault(genero.lower(), set()).add(id_filme)
        for ator in dados_filme.get('atores', []):
            self.atores_para_filmes_idx.setdefault(ator.lower(), set()).add(id_filme)
        diretor = dados_filme.get('diretor')
        if diretor:
            self.diretores_para_filmes_idx.setdefault(diretor.lower(), set()).add(id_filme)

    def _remover_filme_dos_indices(self, dados_filme: dict):
        id_filme = dados_filme['id']
        for genero in dados_filme.get('generos', set()):
            chave_genero = genero.lower()
            if chave_genero in self.generos_para_filmes_idx and id_filme in self.generos_para_filmes_idx[chave_genero]:
                self.generos_para_filmes_idx[chave_genero].remove(id_filme)
                if not self.generos_para_filmes_idx[chave_genero]:
                    del self.generos_para_filmes_idx[chave_genero]
        for ator in dados_filme.get('atores', []):
            chave_ator = ator.lower()
            if chave_ator in self.atores_para_filmes_idx and id_filme in self.atores_para_filmes_idx[chave_ator]:
                self.atores_para_filmes_idx[chave_ator].remove(id_filme)
                if not self.atores_para_filmes_idx[chave_ator]: del self.atores_para_filmes_idx[chave_ator]
        diretor = dados_filme.get('diretor')
        if diretor:
            chave_diretor = diretor.lower()
            if chave_diretor in self.diretores_para_filmes_idx and id_filme in self.diretores_para_filmes_idx[chave_diretor]:
                self.diretores_para_filmes_idx[chave_diretor].remove(id_filme)
                if not self.diretores_para_filmes_idx[chave_diretor]: del self.diretores_para_filmes_idx[chave_diretor]

    def adicionar_filme_catalogo(self, titulo: str, ano: int, diretor: str, generos: set, atores: list) -> dict | None:
        try:
            for no_existente in self.catalogo_filmes_dll:
                if no_existente.data['titulo'].lower() == titulo.lower() and no_existente.data['ano'] == ano:
                    print(f"ERRO: Filme '{titulo}' ({ano}) já existe no catálogo.")
                    return None
            dados_filme = criar_payload_filme(titulo, ano, diretor, generos, atores)
        except ValueError as e:
            print(f"ERRO ao validar dados do filme: {e}")
            return None
        
        novo_no_filme_obj = Node(dados_filme)
        self.catalogo_filmes_dll.add_last(novo_no_filme_obj)
        
        no_filme_adicionado_na_dll = self.catalogo_filmes_dll.tail
        self.filmes_por_id_idx[dados_filme['id']] = no_filme_adicionado_na_dll
        
        self._adicionar_filme_aos_indices(dados_filme)
        print(f"SUCESSO: Filme '{dados_filme['titulo']}' adicionado ao catálogo com ID: {dados_filme['id']}")
        return dados_filme

    def buscar_filme_por_id(self, id_filme: str) -> dict | None:
        no_filme = self.filmes_por_id_idx.get(id_filme)
        return no_filme.data if no_filme else None

    def listar_todos_os_filmes(self):
        if self.catalogo_filmes_dll.empty():
            print("Catálogo de filmes vazio.")
            return
        print("\n--- Catálogo de Filmes ---")
        for i, no_filme in enumerate(self.catalogo_filmes_dll):
            filme = no_filme.data
            status_str = f"[Status: {filme['status'].upper()}]"
            if filme['status'] == 'alugado':
                cliente_alugou = self.clientes_cadastrados.get(filme['id_cliente_alugou'], {})
                cliente_nome = cliente_alugou.get('nome', 'Desconhecido')
                status_str += f" (Alugado por: {cliente_nome} em {filme['data_aluguel']})"
        
            print(f"   Diretor: {filme.get('diretor', 'N/A')}")
            print(f"   Gêneros: {', '.join(filme.get('generos', [])) if filme.get('generos') else 'N/A'}")
            print(f"   Atores: {', '.join(filme.get('atores', [])) if filme.get('atores') else 'N/A'}")
            print("-" * 20)
    
    def listar_filmes_por_status(self, status_desejado: str):
        if self.catalogo_filmes_dll.empty():
            print(f"Nenhum filme no catálogo para listar como '{status_desejado}'.")
            return
        print(f"\n--- Filmes com Status: {status_desejado.upper()} ---")
        encontrados = False
        for i, no_filme in enumerate(self.catalogo_filmes_dll):
            filme = no_filme.data
            if filme['status'] == status_desejado:
                encontrados = True
                info_aluguel = ""
                if status_desejado == 'alugado' and filme['id_cliente_alugou']:
                    cliente_alugou = self.clientes_cadastrados.get(filme['id_cliente_alugou'], {})
                    cliente_nome = cliente_alugou.get('nome', 'Cliente Desconhecido')
                    info_aluguel = f" (Alugado por: {cliente_nome} em {filme['data_aluguel']})"
                print(f"- {filme['titulo']} ({filme['ano']}) ID: {filme['id']}{info_aluguel}")
        if not encontrados:
            print(f"Nenhum filme encontrado com status '{status_desejado}'.")

    def remover_filme_catalogo(self, id_filme: str) -> bool:
        no_a_remover_ref = self.filmes_por_id_idx.get(id_filme)
        if not no_a_remover_ref:
            print(f"ERRO: Filme com ID '{id_filme}' não encontrado.")
            return False
        if no_a_remover_ref.data['status'] == 'alugado':
            print(f"ERRO: Filme '{no_a_remover_ref.data['titulo']}' está atualmente alugado e não pode ser removido.")
            return False

        dados_filme_removido = no_a_remover_ref.data
        try:
            self.catalogo_filmes_dll.remove(no_a_remover_ref)
            
            del self.filmes_por_id_idx[id_filme]
            self._remover_filme_dos_indices(dados_filme_removido)
            print(f"SUCESSO: Filme '{dados_filme_removido['titulo']}' removido do catálogo.")
            return True
        except Exception as e:
            print(f"ERRO ao tentar remover o filme da DLL: {e}")
            return False

    def adicionar_cliente(self, nome: str, contato: str) -> dict | None:
        try:
            for cliente_existente in self.clientes_cadastrados.values():
                if cliente_existente['nome'].lower() == nome.lower():
                    print(f"ERRO: Cliente '{nome}' já cadastrado com ID {cliente_existente['id_cliente']}.")
                    return None
            payload_cliente = criar_payload_cliente(nome, contato)
        except ValueError as e:
            print(f"ERRO ao validar dados do cliente: {e}")
            return None
        self.clientes_cadastrados[payload_cliente['id_cliente']] = payload_cliente
        print(f"SUCESSO: Cliente '{payload_cliente['nome']}' adicionado com ID: {payload_cliente['id_cliente']}")
        return payload_cliente

    def buscar_cliente_por_id(self, id_cliente: str) -> dict | None:
        cliente = self.clientes_cadastrados.get(id_cliente)
        if not cliente:
            print(f"AVISO: Cliente com ID '{id_cliente}' não encontrado.")
        return cliente
        
    def listar_clientes(self):
        if not self.clientes_cadastrados:
            print("Nenhum cliente cadastrado.")
            return
        print("\n--- Lista de Clientes Cadastrados ---")
        for i, (id_cliente, cliente) in enumerate(self.clientes_cadastrados.items()):
            print(f"{i+1}. Nome: {cliente['nome']} (ID: {id_cliente}, Contato: {cliente['contato']})")
            if cliente['historico_alugueis']:
                print(f"   Histórico: {len(cliente['historico_alugueis'])} aluguel(éis)")
            else:
                print("   Histórico: Nenhum aluguel registrado.")

    def alugar_filme(self, id_filme: str, id_cliente: str) -> bool:
        no_filme = self.filmes_por_id_idx.get(id_filme)
        cliente = self.clientes_cadastrados.get(id_cliente)

        if not no_filme:
            print(f"ERRO: Filme com ID '{id_filme}' não encontrado.")
            return False
        if not cliente:
            print(f"ERRO: Cliente com ID '{id_cliente}' não encontrado.")
            return False

        dados_filme = no_filme.data
        if dados_filme['status'] == 'alugado':
            print(f"ERRO: Filme '{dados_filme['titulo']}' já está alugado.")
            return False

        dados_filme['status'] = 'alugado'
        dados_filme['id_cliente_alugou'] = id_cliente
        dados_filme['data_aluguel'] = datetime.date.today().strftime("%Y-%m-%d")
        
        registro_aluguel = (
            id_filme, dados_filme['titulo'],
            dados_filme['data_aluguel'], None
        )

        cliente['historico_alugueis'].append(registro_aluguel)
        print(f"SUCESSO: Filme '{dados_filme['titulo']}' alugado para '{cliente['nome']}' em {dados_filme['data_aluguel']}.")
        return True

    def devolver_filme(self, id_filme: str) -> bool:
        no_filme = self.filmes_por_id_idx.get(id_filme)
        if not no_filme:
            print(f"ERRO: Filme com ID '{id_filme}' não encontrado.")
            return False
        
        dados_filme = no_filme.data
        if dados_filme['status'] == 'disponivel':
            print(f"ERRO: Filme '{dados_filme['titulo']}' não está atualmente alugado.")
            return False

        id_cliente_que_alugou = dados_filme['id_cliente_alugou']
        cliente = self.clientes_cadastrados.get(id_cliente_que_alugou)
        data_devolucao_atual = datetime.date.today().strftime("%Y-%m-%d")

        if cliente:
            for i, aluguel_tupla in reversed(list(enumerate(cliente['historico_alugueis']))):
                hist_id_filme, hist_titulo, hist_data_aluguel, hist_data_devolucao = aluguel_tupla
                if hist_id_filme == id_filme and hist_data_devolucao is None:
                    novo_registro = (hist_id_filme, hist_titulo, hist_data_aluguel, data_devolucao_atual)
                    cliente['historico_alugueis'][i] = novo_registro
                    break
        
        dados_filme['status'] = 'disponivel'
        dados_filme['id_cliente_alugou'] = None
        dados_filme['data_aluguel'] = None
        print(f"SUCESSO: Filme '{dados_filme['titulo']}' devolvido em {data_devolucao_atual}.")
        return True

    def ver_historico_cliente(self, id_cliente: str):
        cliente = self.buscar_cliente_por_id(id_cliente)
        if not cliente: return
        print(f"\n--- Histórico de Aluguéis do Cliente: {cliente['nome']} (ID: {id_cliente}) ---")
        if not cliente['historico_alugueis']:
            print("Nenhum aluguel registrado para este cliente.")
            return
        
        for aluguel_tupla in cliente['historico_alugueis']:
            id_filme, titulo_filme, data_aluguel, data_devolucao = aluguel_tupla
            devolucao_str = data_devolucao if data_devolucao else "Pendente"
            print(f"- Filme: {titulo_filme} (ID: {id_filme})")
            print(f"  Alugado em: {data_aluguel}, Devolvido em: {devolucao_str}")
            print("-" * 15)
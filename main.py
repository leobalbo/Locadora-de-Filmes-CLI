import datetime
from gerenciador_locadora import GerenciadorLocadora
from cli import iniciar_interface

def popular_dados_exemplo_locadora(gerenciador: GerenciadorLocadora):
    print("Populando dados iniciais para a locadora...")

    amanha = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d-%m-%Y")
    hoje_str = datetime.date.today().strftime('%d-%m-%Y')
    
    f1_data = gerenciador.adicionar_filme_catalogo("Matrix Reloaded", "Wachowskis", {"Ação", "Ficção Científica"}, ["Keanu Reeves"], "15-05-2003")
    f2_data = gerenciador.adicionar_filme_catalogo("O Senhor dos Anéis: A Sociedade do Anel", "Peter Jackson", {"Fantasia", "Aventura"}, ["Elijah Wood"], "19-12-2001")
    f3_data = gerenciador.adicionar_filme_catalogo("A Viagem de Chihiro", "Hayao Miyazaki", {"Animação", "Fantasia"}, [],  "18-07-2003")
    f4_data = gerenciador.adicionar_filme_catalogo("Duna: Parte Dois", "Denis Villeneuve", {"Ficção Científica", "Aventura"}, ["Timothée Chalamet"], amanha)
    f5_data = gerenciador.adicionar_filme_catalogo("Interestelar", "Christopher Nolan", {"Ficção Científica"}, ["Matthew McConaughey"], hoje_str)

    c1_data = gerenciador.adicionar_cliente("Ana Silva", "ana.silva@email.com")
    c2_data = gerenciador.adicionar_cliente("Bruno Costa", "99999-8888")
    c3_data = gerenciador.adicionar_cliente("Lucas Moura", "lucas.moura@email.com")

    if f1_data and c1_data:
        gerenciador.alugar_filme(f1_data['id'], c1_data['id_cliente'])
    
    if f4_data and c3_data:
        gerenciador.reservar_lancamento(f4_data['id'], c3_data['id_cliente'])
    
    print("-" * 30)
    print("Dados de exemplo da locadora populados.")
    print("-" * 30)

if __name__ == "__main__":
    meu_gerenciador_locadora = GerenciadorLocadora()
    popular_dados_exemplo_locadora(meu_gerenciador_locadora)

    try:
        iniciar_interface(meu_gerenciador_locadora)
    except Exception as e:
        print(f"\nERRO CRÍTICO NO PROGRAMA: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nPrograma da locadora finalizado.")
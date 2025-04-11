import sqlite3

# Conectar com o banco de dados
def obter_conexao():
    conexao = sqlite3.connect("meu_estoque.db")
    return conexao

# Inicializar o banco com a tabela
def inicializar_banco():
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL,
        qtd INTEGER NOT NULL,
        valor REAL NOT NULL
    )
    ''')
    conexao.commit()
    conexao.close()

# Adicionar o item e suas características
def adicionar_item():
    try:
        nome_item = input("Nome do item: ").strip()
        if not nome_item or nome_item.isnumeric():
            print("Erro: Nome inválido. Não pode ser vazio nem um número.")
            return
        quantidade_item = int(input("Quantidade: "))
        preco_item = float(input("Preço: "))
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO itens (nome, qtd, valor) VALUES (?, ?, ?)", 
                       (nome_item, quantidade_item, preco_item))
        conexao.commit()
        print(f"Item '{nome_item}' adicionado com sucesso!")

    except sqlite3.IntegrityError:
        print("Erro: Esse item já foi cadastrado. Entre no menu para alterá-lo.")
    except ValueError:
        print("Erro: Insira valores numéricos válidos para quantidade e preço.")
    finally:
        try:
            conexao.close()
        except:
            pass

# Editar algum item que já foi cadastrado
def editar_item():
    try:
        nome = input("Nome do item a modificar: ").strip()
        nova_qtd = int(input("Nova quantidade: "))
        novo_valor = float(input("Novo preço: "))
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("UPDATE itens SET qtd = ?, valor = ? WHERE nome = ?", (nova_qtd, novo_valor, nome))
        if cursor.rowcount == 0:
            print("Erro: Nenhum item encontrado com esse nome.")
        else:
            conexao.commit()
            print("Item atualizado com sucesso.")
    except ValueError:
        print("Erro: Digite apenas números.")
    finally:
        conexao.close()

# Remover um item
def remover_item():
    try:
        nome = input("Nome do item a remover: ").strip()
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM itens WHERE nome = ?", (nome,))
        if cursor.rowcount == 0:
            print("Erro: Nenhum item encontrado com esse nome.")
        else:
            conexao.commit()
            print("Item removido com sucesso.")
    finally:
        conexao.close()

# Entrar no menu
def executar_menu():
    inicializar_banco()
    while True:
        print("\n----- CONTROLE DE ESTOQUE -----")
        print("1. Cadastrar novo item")
        print("2. Listar itens")
        print("3. Alterar item")
        print("4. Excluir item")
        print("5. Sair")
        opcao = int(input("Selecione uma opção: "))

        if opcao == 1:
            adicionar_item()
        elif opcao == 2:
            mostrar_itens()
        elif opcao == 3:
            editar_item()
        elif opcao == 4:
            remover_item()
        elif opcao == 5:
            print("Saindo... até a próxima!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    executar_menu()

############ CASOS DE TESTE DA FUNÇÃO INSERIR #############

#TESTE POSITIVO
#adicionar_item(nome"Calça", Qtd"5",Valor"10.99")
#TESTE NEGATIVO
#adicionar_item(nome"Calça", Qtd"5",Valor"10.99")
#TESTE NEGATIVO, VALOR TEM Q SER NUMERICO
#adicionar_item(nome"Calça", Qtd"5",Valor"DEZ E NOVETA E NOVE")
#TESTE NEGATIVO, NOME TEM QUE SER STRING
#adicionar_item(nome"2000", Qtd"5",Valor"10.99")

import trie
import hash
import time
import csv
from mergesort import dec_mergesort
import re
from rich.table import Table
from rich.console import Console
import os

def initialize_data_structures():
    start_time = time.time()

    trie_names = trie.trie_tree()
    player_hash = hash.PlayerHash(12007)
    with open('players.csv', newline='') as fifa_players:
        reader = csv.reader(fifa_players)
        # skips header
        next(reader)
        for row in reader:
            # last two fields: [amount of reviews, score]
            player_hash.insert(int(row[0]), row + [0, 0])    
            # (name, player_id)
            trie_names.insert(row[2], row[0])

    #loop to create the user hash and name tree and insert reviews into players
    user_hash = hash.UserHash(115001)
    with open('minirating.csv', newline='') as user_reviews:
        reader = csv.reader(user_reviews)
        # skips header
        next(reader)
        for row in reader:
            # (player_id, score)
            player_hash.insert_review(int(row[1]), float(row[2]))
            # (user_id, info)
            user_hash.insert(int(row[0]), tuple(row))
        player_hash.calc_avg_score()
    
    #loop to create the trie tree and fill it with players tags
    trie_tags = trie.trie_tree()
    with open('tags.csv', newline='') as tags:
        reader = csv.reader(tags)
        # skips header
        next(reader)
        for row in reader:
            # (tag, player_id)
            trie_tags.insert(row[2], row[1])

    end_time = time.time()
    result_time = end_time - start_time

    return player_hash, user_hash, trie_tags, trie_names, result_time

def make_table(info_arr:list, title:str, user_input:str):

    table = Table(title=title)
    table.add_column('Id SOFIFA', justify='center', style='bold bright_blue')
    table.add_column('Nome curto', justify ='center', style = 'bold orange1')
    table.add_column('Nome longo', justify ='center', style = 'bold green')

    if user_input.startswith("player") or user_input.startswith("tags") or user_input.startswith("top"):
        table.add_column('Posições', justify ='center', style = 'bold bright_yellow')

    if user_input.startswith("tags") or user_input.startswith("top"):
        table.add_column('Nacionalidade', justify ='center', style = 'bold bright_red')
        table.add_column('Nome do clube', justify ='center', style = 'bold bright_cyan')
        table.add_column('Nome da liga', justify ='center', style = 'bold dark_red')

    table.add_column('Média global', justify ='center', style = 'bold hot_pink')
    table.add_column('Nº de Avaliações', justify ='center', style = 'bold bright_red')

    if user_input.startswith("user"):
        table.add_column('Avaliação do usuário', justify ='center', style = 'bold bright_cyan')
    
    for info in info_arr:
        # id, short_name, long_name, position, rating, count
        if user_input.startswith("player"):
            table.add_row(str(info[0]), str(info[1]), str(info[2]), str(info[3]), f'{info[-1]:.6}', str(info[-2]))
        elif user_input.startswith("user"):
        # id, short_name, long_name, global rating, count, user review
            table.add_row(str(info[0]), str(info[1]), str(info[2]), f'{info[-2]:.6}', str(info[-3]), str(info[-1]))
        else:
            table.add_row(str(info[0]), str(info[1]), str(info[2]), str(info[3]), str(info[4]), str(info[5]), str(info[6]), f'{info[-1]:.6}', str(info[-2]))
            pass
    
    return table

def main():
    player_hash, user_hash, trie_tags, trie_names, result_time = initialize_data_structures()
    print(f'Tempo de inicialização das estruturas de dados: {result_time:.2f} segundos')

    console = Console()
    os.system('clear')

    # enquanto não finlandês    
    options = """Opções:
1. Buscar jogador por nome - insira: player <prefixo>
2. Buscar avaliações feitas por um usuário - insira: user <user_id>
3. Buscar top N jogadores para posição - insira: top <N> <position>
4. Buscar jogadores por lista de tags - tags '<tag1>''<tag2>'...'<tagN>'
5. Sair - insira: sair

Opção desejada: """

    title = r"""     
   _______________     _______ _____   __  ______  ________  _  ______   _________  _____  _______ 
  / __/  _/ __/ _ |   / ___/ // / _ | /  |/  / _ \/  _/ __ \/ |/ / __/  / __/  _/ |/ / _ \/ __/ _ \
 / _/_/ // _// __ |  / /__/ _  / __ |/ /|_/ / ___// // /_/ /    /\ \   / _/_/ //    / // / _// , _/
/_/ /___/_/ /_/ |_|  \___/_//_/_/ |_/_/  /_/_/  /___/\____/_/|_/___/  /_/ /___/_/|_/____/___/_/|_|                                                                                                                                                                                       
    """
    console.print(title, style='bright_red')    

    while True:
        user_input = input(options).strip().lower()

        os.system('clear')

        if user_input.startswith("player"):
            prefix = user_input.split(" ", 1)[1]
            # retorna lista com ids
            search_result = trie_names.search(prefix)
            if not search_result:
                print(f'Sem resultados para a pesqusisa por "{prefix}".')
                continue
            # retorna lista com informações dos jogadores
            search_result = [player_hash.search(int(player_id)) for player_id in search_result]
            # sort de acordo com score medio e torna decrescente
            search_result = dec_mergesort(search_result, -1)

            table = make_table(search_result, f'Resultados da busca por "{prefix}"', user_input)            
            
            console.print(table)
            input('Pressione enter para continuar...')
            os.system('clear')

        elif user_input.startswith("user"):
            #retorna o id informado pelo usuario
            user_id = user_input.split(" ", 1)[1]
            #retorna lista com player ids e reviews pra cada um
            user_reviews = user_hash.get_reviews(int(user_id))
            if not user_reviews:
                os.system('clear')
                print(f'Sem resultados para o usuário "{user_id}"')
                continue
            player_info = []
            for player_id, review in user_reviews:  #procura dados do jogador na hash a partir do id, pega a review associada ao jogador e da append no fim da lista retornada pela hash
                player_data = player_hash.search(int(player_id))
                player_data.append(review)
                player_info.append(player_data)

            player_info = dec_mergesort(player_info, -1)    #ordena primeiro pela review do usuario e depois pela media global, de forma estavel
            player_info = dec_mergesort(player_info, -2)

            if len(player_info) > 20:   #se forem mais que 20 jogadores, imprime apenas os primeiros 20
                player_info = player_info[:20]

            ## prints table
            table = make_table(player_info, f'Jogadores avaliados por usuário "{user_id}"', user_input)            

            console.print(table)
            input('Pressione enter para continuar...')
            os.system('clear')
    
        elif user_input.startswith("top"):
            top_string, position = user_input.split(" ")
            # slices topN to get N
            N_players = int(top_string[3:])

            if not N_players:
                os.system('clear')
                print('Insira um numero.')
                continue
            # retorna lista com informações dos top jogadores para posição
            players_list = player_hash.position_over_1000(position)

            if not players_list:
                os.system('clear')
                print(f'Sem resultados para a posição "{position}".')
                continue
            # ordena por media global e pega os N primeiros
            players_list = dec_mergesort(players_list, -1)
            if players_list > N_players:
                players_list = players_list[:N_players]
            table = make_table(players_list, f'Top {N_players} jogadores para a posição "{position}"', user_input)

            console.print(table)
            input('Pressione enter para continuar...')
            os.system('clear')
        
        elif user_input.startswith("tags"):
            player_info = []
            aux_set = None
            tags = re.findall("'(.*?)'", user_input[1:]) #isso aqui pega todas as strings entre ''. eu tinha feito de um outro jeito, mas ele nao funcionava se nao tivesse um espaco entre cada tag
                                                         #os ' marcam o que deve estar no inicio e no fim da string, * indica que eh pra pegar
                                                         #todos os caracteres e ? impede que ele junte todas as tags em uma string só, parando de coletar a cada fim de '
            if not tags:
                print('Nenhuma tag fornecida.')
                break

            for tag in tags:
                players_list = trie_tags.search_non_recursive(tag) #procura jogadores com a tag
                if not players_list:
                    print(f'Sem resultados para jogadores com a tag {tag}.')
                    break

                player_set = set()
                for player in players_list:
                    player_set.add(int(player)) #vai adicionando a um novo set por tag

                if aux_set is None:
                    aux_set = player_set #se aux_set ainda nao tem nada, inicializa ele
                else:
                    aux_set &= player_set #pra todas as outras iteracoes, aux_set guarda a interseccao entre os jogadores com a tag atual e a anterior

            if not aux_set:
                print('Sem jogadores com essa combinação de tags.')
                continue

            players_list = [player_hash.search(int(player)) for player in aux_set]
            #busca cada jogador na hash
            players_list = dec_mergesort(players_list,-1)
            #ordena por nota global media
            table = make_table(players_list, f'Resultados da busca pelas tags {tags}', user_input)            
            
            console.print(table)
            input('Pressione enter para continuar...')
            os.system('clear')

        elif user_input == "sair":
            os.system('clear')
            break
        else:
            print('Opção inválida.')

# call main function
main()
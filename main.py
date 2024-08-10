import trie
import hash
import time
import csv
from mergesort import dec_mergesort
import re

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

if __name__ == "__main__":
    player_hash, user_hash, trie_tags, trie_names, result_time = initialize_data_structures()
    print(f'Tempo de inicialização das estruturas de dados: {result_time:.2f} segundos')

    # enquanto não finlandês    
    options = """
1. Buscar jogador por nome - insira: player <prefixo>
2. Buscar avaliações feitas por um usuário - insira: user <user_id>
3. Buscar top N jogadores para posição - insira: top <N> <position>
4. Buscar jogadores por lista de tags - tags '<tag1>''<tag2>'...'<tagN>'
5. Sair - insira: sair

Opção desejada: """

    while True:
        user_input = input(options).strip().lower()

        if user_input.startswith("player"):
            prefix = user_input.split(" ", 1)[1]
            # retorna lista com ids
            search_result = trie_names.search(prefix)
            # retorna lista com informações dos jogadores
            search_result = [player_hash.search(int(player_id)) for player_id in search_result]
            # calcula media do score
            for player in search_result:
                if player[-2] != 0:
                    player[-1] = player[-1] / player[-2]
                else:
                    player[-1] = 0.0
            # sort de acordo com score medio e torna decrescente
            search_result = dec_mergesort(search_result, -1)
            for player in search_result:
                # id, short_name, long_name, position, rating, count
                print(player[0], player[1], player[2], player[3], f'{player[-1]:.6}', player[-2])

        elif user_input.startswith("user"):
            user_id = user_input.split(" ", 1)[1]
            #retorna o id informado pelo usuario
            user_reviews = user_hash.get_reviews(int(user_id))
            #retorna lista com player ids e reviews pra cada um
            player_info = []
            for player_id, review in user_reviews:  #procura dados do jogador na hash a partir do id, pega a review associada ao jogador e da append no fim da lista retornada pela hash
                player_data = player_hash.search(int(player_id))
                player_data.append(review)
                player_info.append(player_data)

            player_info = dec_mergesort(player_info, -1)    #ordena primeiro pela review do usuario e depois pela media global, de forma estavel
            player_info = dec_mergesort(player_info, -2)

            if len(player_info) > 20:   #se forem mais que 20 jogadores, imprime apenas os primeiros 20
                player_info = player_info[:20]

            for player in player_info:
                print(player[0], player[1], player[2], player[3], f'{player[-2]:.6}', player[-3], player[-1])

    
        elif user_input.startswith("top"):
            _, N, position = user_input.split(" ")
            # Adicione aqui o código para buscar top N jogadores para a posição

        
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
                print('Sem jogadores com essa combinacao de tags.')
                continue

            players_list = [player_hash.search(int(player)) for player in aux_set]
            #busca cada jogador na hash
            players_list = dec_mergesort(players_list,-1)
            #ordena por nota global media
            for player in players_list:
                # id, short_name, long_name, position, rating, count
                print(player[0], player[1], player[2], player[3], f'{player[-1]:.6}', player[-2])   

        elif user_input == "sair":
            print("Saindo...")
            break
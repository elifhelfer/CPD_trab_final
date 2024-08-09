import trie
import hash
import time
import csv
import mergesort

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
    with open('rating.csv', newline='') as user_reviews:
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
4. Buscar jogadores por lista de tags - tags <tag1>,<tag2>,...,<tagN>
5. Sair - insira: sair
opção desejada: """

    while True:
        user_input = input(options).strip()

        if user_input.startswith("player"):
            prefix = user_input.split(" ", 1)[1]
            # retorna lista com ids
            search_result = trie_names.search(prefix)
            # retorna lista com informações dos jogadores
            search_result = [player_hash.search(int(player_id)) for player_id in search_result]
            # calcula media do score
            for player in search_result:
                player[-1] = player[-1] / player[-2]
            # sort de acordo com score medio e torna decrescente
            search_result = mergesort.mergesort(search_result, -1)[::-1]
            for player in search_result:
                # id, short_name, long_name, position, rating, count
                print(player[0], player[1], player[2], player[3], f'{player[-1]:.6}', player[-2])

        elif user_input.startswith("user"):
            user_id = user_input.split(" ", 1)[1]
            # Adicione aqui o código para buscar avaliações de um usuário usando o user_id
        
        elif user_input.startswith("top"):
            _, N, position = user_input.split(" ")
            # Adicione aqui o código para buscar top N jogadores para a posição
        
        elif user_input.startswith("tags"):
            tags = user_input.split(" ", 1)[1].split(",")
            # Adicione aqui o código para buscar jogadores por lista de tags        
        elif user_input == "sair":
            print("saindo...")
            break
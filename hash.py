class FifaHash:
    def __init__(self, hash_size):
        self.hash_size = hash_size
        self.buckets = [[] for _ in range(self.hash_size)]

    def hash_function(self, key):
        """Basic hash function: key % size_of_hash"""
        return key % self.hash_size
    
    def insert(self, key, info):
        """appends the new info to the end of the list in the bucket"""
        index = self.hash_function(key)
        self.buckets[index].append(info)

    def search(self, key):
        """Searches the required id and returns info, otherwise returns None"""
        index = self.hash_function(key)
        
        for element in self.buckets[index]:
            if int(element[0]) == key:
                return element
        return None
    
class PlayerHash(FifaHash):
    def __init__(self, hash_size):
        super().__init__(hash_size)
    
    def insert_review(self, key, score):
        index = self.hash_function(key)
        
        for element in self.buckets[index]:
            if int(element[0]) == key:
                element[-1] += score
                element[-2] += 1
                return 
        print("Player reviewd not found")
        return

class UserHash(FifaHash):
    def __init__(self, hash_size):
        super().__init__(hash_size)

    def insert(self, key, info):
        index = self.hash_function(key)
        # if the element was already inserted in bucket
        for element in self.buckets[index]:
            if int(element[0]) == key:
                element.append(info)
                return 
        # if it hasn't been inserted yet
        self.buckets[index].append([key, info])
        return

if __name__ == "__main__":
    import csv
    import time
    
    start_time = time.time()
    player_hash = PlayerHash(4999)
    with open('/home/guifernandes0521/final_cpd/CPD_trab_final/players.csv', newline='') as fifa_players:
        reader = csv.reader(fifa_players)
        # skips header
        next(reader)

        for row in reader:
            # last two fields: [amount of reviews, score of review]
            player_hash.insert(int(row[0]), row + [0,0])      

    user_hash = UserHash(59999)
    
    with open('/home/guifernandes0521/final_cpd/CPD_trab_final/rating.csv', newline='') as user_reviews:
        reader = csv.reader(user_reviews)
        # skips header
        next(reader)
        
        for row in reader:
            # (player_id, score)
            player_hash.insert_review(int(row[1]), float(row[2]))
            # (user_id, info)
            user_hash.insert(int(row[0]), (row[1], row[2]))
    
    end_time = time.time()
    
    # Calcular e imprimir o tempo total de execução
    execution_time = end_time - start_time
    print(f"Tempo de execução do segundo bloco de leitura de arquivo: {execution_time:.2f} segundos")

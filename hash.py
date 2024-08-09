class FifaHash:
    def __init__(self, hash_size):
        self.hash_size = hash_size
        self.buckets = [[] for _ in range(self.hash_size)]

    def hash_function(self, key):
        """Basic hash function: key % size_of_hash"""
        return key % self.hash_size
    
    def insert(self, key, info):
        """Appends the new info to the end of the list in the bucket"""
        index = self.hash_function(key)
        self.buckets[index].append(info)

    def search(self, key=None):
        """Returns info for required id, otherwise returns None"""
        if key == None:
            raise ValueError("Key must be passed")

        index = self.hash_function(key)
        for element in self.buckets[index]:
            if int(element[0]) == key:
                return element
        print("Element not found")
        return None

    @property
    def occupancy(self):
        """Returns the occupancy of the hash table"""
        occupied = 0
        for i in range(self.hash_size):
            if self.buckets[i]:
                occupied += 1
        return f'{(100 * occupied/self.hash_size):.2f}'

    @property
    def average_list_size(self):
        """Returns the occupancy of the hash table"""
        occupied = 0
        sum_len = 0
        for i in range(self.hash_size):
            if self.buckets[i]:
                occupied += 1
                sum_len += len(self.buckets[i])
        return f'{sum_len//occupied}'

    #quando tu usa o decorador @property, tu cria um método que pode ser chamado sem (), sendo tipo um atributo normal. -> encapsulamento
    @property
    def size(self):
        return self.hash_size

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
    
    def search(self, key=None, *keys):
        """If a list of keys is passed, returns a list of players.
        If a list of keys is passed, returns a list of all elements with the same key"""
        
        if not key and not keys:
            raise ValueError("Key or keys must be passed")
        # if a list of keys is passed, returns a list of players
        if keys:
            players = []
            for k in keys:
                index = self.hash_function(k)
                for element in self.buckets[index]:
                    if int(element[0]) == k:
                        players.append(element)
            return players
        # if a single key is passed, returns a single player   
        else:
            index = self.hash_function(key)
            for element in self.buckets[index]:
                if int(element[0]) == key:
                    return element
            print("Player not found")
            return None
class UserHash(FifaHash):
    def __init__(self, hash_size):
        super().__init__(hash_size)
    
    def get_reviews(self, key):
        """Returns a list of tuples with player_id and score"""
        index = self.hash_function(key)
        reviews = []
        for element in self.buckets[index]:
            if int(element[0]) == key:
                # appends tuple (player_id, score)
                reviews.append((element[1], element[2]))
        if reviews:
            return reviews
        return None
    
if __name__ == "__main__":
    import csv
    import time
    
    start_time = time.time()
    #loop to create the player hash 
    player_hash = PlayerHash(12007)
    with open('/home/guifernandes0521/final_cpd/CPD_trab_final/players.csv', newline='') as fifa_players:
        reader = csv.reader(fifa_players)
        # skips header
        next(reader)
        for row in reader:
            # last two fields: [amount of reviews, score of review]
            player_hash.insert(int(row[0]), row + [0, 0])    
    #loop to create the user hash and insert reviews into players
    user_hash = UserHash(115001)
    with open('/home/guifernandes0521/final_cpd/CPD_trab_final/rating.csv', newline='') as user_reviews:
        reader = csv.reader(user_reviews)
        # skips header
        next(reader)
        
        for row in reader:
            # (player_id, score)
            player_hash.insert_review(int(row[1]), float(row[2]))
            # (user_id, info)
            user_hash.insert(int(row[0]), (row[0], row[1], row[2]))
    
    end_time = time.time()
    # Calcular e imprimir o tempo total de execução
    execution_time = end_time - start_time
    print(f"Tempo de execução processamento: {execution_time:.2f} segundos")
    
    print('occupancy of user_hash:', user_hash.occupancy)
    print('average list size:', user_hash.average_list_size)
    print('player_hash_occupancy',player_hash.occupancy);  
    print('player_hash_list_average',player_hash.average_list_size);

    print('players evaluated by user',user_hash.get_reviews(66782))
    print('players search result with 1 key',player_hash.search(254234))
    print('players search result with many keys',player_hash.search(210429,210646,211189,211438,211619))


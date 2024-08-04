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
        pass
    pass

class UserHash(FifaHash):
    def __init__(self, hash_size):
        super().__init__(hash_size)
        pass
    pass

if __name__ == "__main__":
    import csv
    
    player_hash = FifaHash(1999)

    with open('/home/guifernandes0521/final_cpd/CPD_trab_final/players.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        # skips header
        next(reader)

        for row in reader:
            key = int(row[0])
            info = row[0:]
            player_hash.insert(key, info)      
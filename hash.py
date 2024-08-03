import pandas as pd

class FifaHash:
    def __init__(self, hash_size):
        self.hash_size = hash_size
        self.player_count = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def hash_function(self, key):
        """Basic hash function: key % size_of_hash"""
        return key % self.hash_size
    
    def insert(self, fifa_id, player_info):
        """Insert appends the new info to the end of the list in the bucket"""
        index = self.hash_function(fifa_id)
        self.buckets[index].append(player_info)
        self.player_count += 1

    def search(self, fifa_id):
        """Searches the required id and returns player's, otherwise returns None"""
        index = self.hash_function(fifa_id)
        
        for player in self.buckets[index]:
            if player[0] == fifa_id:
                return player
        return None

    
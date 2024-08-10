import csv

class trie_node:
    def __init__(self, letter: str):
        self.letter = letter
        self.children = []
        self.is_end = []

class trie_tree:
    def __init__(self):
        self.root = trie_node(None)

    def insert(self, key: str, end_id: int):
        aux_node = self.root
        for i in range(len(key)):
            found = False
            for child in aux_node.children:
                if child.letter == key[i]:
                    aux_node = child
                    found = True
            if found == False:
                new_node = trie_node(key[i])
                aux_node.children.append(new_node)
                aux_node = new_node
            if i == len(key)-1:
                        aux_node.is_end.append(end_id)
                
    def collect_words(self, node: trie_node, prefix: str, words: list):
        if node.is_end:
            words.extend(node.is_end)
        for child in node.children:
            self.collect_words(child, prefix+child.letter, words)
        return words

    def search(self, key: str):
        aux_node = self.root
        key = key.lower()
        words = []
        prefix = ''
        for letter in key:
            found = False
            for child in aux_node.children:
                if child.letter.lower() == letter:
                    prefix += child.letter
                    aux_node = child
                    found = True
                    break
        if not found:
            return None
        results = self.collect_words(aux_node, prefix, words)
        return results
    
    def search_non_recursive(self, key: str):
        aux_node = self.root
        key = key.lower()
        prefix = ''
        for letter in key:
            found = False
            for child in aux_node.children:
                if child.letter.lower() == letter:
                    prefix += child.letter
                    aux_node = child
                    found = True
                    break
        if not found:
            return None
        if aux_node.is_end:
            return aux_node.is_end
        else:
            return None

if __name__ == "__main__":
    
    tree = trie_tree()

    with open('players.csv', mode='r', newline='') as file:
       csv_reader = csv.reader(file)
       next(csv_reader)
       for row in csv_reader:
           tree.insert(row[2], row[0])
    
    print(tree.search('lucas'))

    # csv_file = './arquivos-parte1/tags.csv'
    # tree = trie_tree()
    # with open(csv_file, mode='r', newline='') as file:
    #     csv_reader = csv.reader(file)
        
    #     for row in csv_reader:
    #         tree.insert(row[2], row[1])

    # print(tree.search('BRAZIL'))
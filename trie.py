class trie_node():
    def __init__(self, letter: str):
        self.letter = letter
        self.children = []
        self.is_end = False

class trie_tree():
    def __init__(self):
        self.root = trie_node(None)

    def insert(self, word: str):
        aux_node = self.root
        for i in range(len(word)):
            found = False
            for child in aux_node.children:
                if child.letter == word[i]:
                    aux_node = child
                    found = True
                    if i >= len(word) - 1:
                        child.is_end = True         #trocar para ID sofifa
            if found == False:
                new_node = trie_node(word[i])
                aux_node.children.append(new_node)
                aux_node = new_node
                
                               
    def search(self, word: str):
        aux_node = self.root
        results = []
        partial_result = ''
        found = False
        for letter in word:
            for child in aux_node.children:
                if child.letter == letter:
                    aux_node = child
                    found = True
        if not found:
            return None
        results = collect_words(child, word)
            
        def collect_words(node: trie_node, prefix: str):
            


tree = trie_tree()
tree.insert('tese')
tree.insert('teste')
tree.insert('testes')
tree.insert('samba')
tree.insert('sans')

print(tree.search('tr'))
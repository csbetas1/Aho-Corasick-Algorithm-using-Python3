#   Aho-Corasick Algorithm implementation in Python3
#   Coded by George Prince


# node of the trie
class TrieNode:

    def __init__(self):

        self.failNode = None        # node which is to be taken in case of a failed condition

        self.output = []            # list of strings which are present in main text on the presence of this node

        self.children = dict()      # hash-map having characters (which make up words when combined) each mapping a node of the  trie


# main trie
class Trie:

    def __init__(self):

        self.root = None
        self.create_root()

    def create_root(self):

        self.root = TrieNode()
        return self.root

    # function to insert a new word in the trie
    def insert(self, word):

        node = self.root
        for value in word:
            if value in node.children:
                node = node.children[value]
            else:
                node.children[value] = TrieNode()
                node = node.children[value]
        node.output.append(word)

    # function for creating fail state machine
    def create_fail_states(self):

        node = self.root
        queue = []

        # setting the failNodes of the children nodes of root as root itself
        for i in node.children:
            node.children[i].failNode = self.root
            queue.append(node.children[i])

        # assigning failNodes of other remaining nodes using breadth first search
        while len(queue):
            node = queue.pop(0)

            for i in node.children:
                queue.append(node.children[i])
                fail_node = node.failNode

                while fail_node is not None and i not in fail_node.children:
                    fail_node = fail_node.failNode

                node.children[i].failNode = fail_node.children[i] if fail_node is not None else self.root

                # adding output strings of failNode with current node
                node.children[i].output += node.children[i].failNode.output

    # function to search patterns in a given text using the  trie
    def search_words(self, word):

        node = self.root
        pos = 0       # variable to count the position of current character
        for i in word:
            while node is not None and i not in node.children:
                node = node.failNode

            node = node.children[i] if node is not None else self.root

            for out in node.output:
                print(out, 'is starting from index', pos - len(out) + 1)

            pos += 1


def find_substrings(words, parts):

    root = Trie()
    for i in parts:
        root.insert(i)

    root.create_fail_states()

    for i in words:
        print("For "+i+' :')
        root.search_words(i)
        print('')


if __name__ == '__main__':
    texts = ["Apple", "Angle", "Apparant"]
    patterns = ["Apple", "pple", "ple", "le", "e", "App", "Appl", "Ap", "A", "p", "l", "An", "ng"]
    find_substrings(texts, patterns)


'''
Output :


For Apple :
A is starting from index 0
Ap is starting from index 0
p is starting from index 1
App is starting from index 0
p is starting from index 2
Appl is starting from index 0
l is starting from index 3
Apple is starting from index 0
pple is starting from index 1
ple is starting from index 2
le is starting from index 3
e is starting from index 4

For Angle :
A is starting from index 0
An is starting from index 0
ng is starting from index 1
l is starting from index 3
le is starting from index 3
e is starting from index 4
'''

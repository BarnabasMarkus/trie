#!/usr/bin/env python3
# T R I E

# Project   Trie Implementation
# Author    Barnabas Markus
# Email     barnabasmarkus@gmail.com
# Date      13.07.2017
# Python    3.6
# License   MIT


WORDS = []


class Trie(object):


    def __init__(self, char, closing=False):
        self.char = char
        self.children = {}
        # closing: (bool) end of the word
        self.closing = closing


    def insert(self, word):
        """ Insert given word into trie structure """
        head, tail = word[0], word[1:]
        closing = False if tail else True

        # insert head if it does not exist
        if head not in self.children:
            self.children[head] = Trie(head, closing=closing)
        # update closing flag if it's True (default = False)
        elif closing:
            self.children[head].closing = closing

        # head inserted, go on to tail
        if tail:
            self.children[head].insert(tail)


    def parse(self, word=''):
        """ Parse trie, collecting all words recursively 
        and return them in a list """
        global WORDS

        word += self.char
        if self.closing:
            WORDS.append(word)
        for char in self.children:
            self.children[char].parse(word)


    def from_file(self, file_path):
        """ Build trie from file. Every line will be a new word in trie """
        with open(file_path, 'r') as f:
            for line in f:
                word = line.strip()
                self.insert(word)

    def to_file(self, file_path):
        """ Write all words from trie to file """
        with open(file_path, 'w') as f:
            for word in self.to_list():
                f.write(word + '\n')


    def from_list(self, words: list):
        """ Build trie from list of words """
        for word in words:
            self.insert(word)


    def to_list(self):
        """ Represent trie as a list of words """
        global WORDS
        WORDS = []
        self.parse()
        return WORDS


    def __len__(self):
        """ Return the number of words in trie """
        return len(self.to_list())


    def __contains__(self, word):
        """ Return True if word is in trie, else False """
        if len(word) == 0:
            return False

        head, tail = word[0], word[1:]
        if head in self.children:
            if head == word:
                if self.children[head].closing:
                    return True
                else:
                    return False
            else:
                return self.children[head].__contains__(tail)
        else:
            return False


    def __getitem__(self, prefix):
        """ Return list of all autocompleted form of a given prefix """
        closings = self.get_postfix(prefix)
        return [prefix + closing for closing in closings]


    def get_postfix(self, prefix):
        """ Return a list if all possible postfix of a given """
        if len(prefix) == 0:
            return []

        head, tail = prefix[0], prefix[1:]
        if head in self.children:
            if head == prefix:
                postfixs = self.children[head].to_list()
                return [postfix[1:] for postfix in postfixs]
            else:
                return self.children[head].get_postfix(tail)
        else:
            return []


    def __delitem__(self, word):
        """ Delete word from trie. Actually it set the closing flag of the
        given word from True to False """
        if len(word) == 0:
            return None

        head, tail = word[0], word[1:]
        if head in self.children:
            if head == word:
                self.children[head].closing = False
            else:
                self.children[head].__delitem__(tail)
        else:
            raise charError


    def display(self, indent=0):
        """ Pretty print of trie """
        print(' '*indent, self.char)
        for value in self.children:
            self.children[value].display(indent+2)

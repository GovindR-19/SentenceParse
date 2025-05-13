import nltk
from nltk import word_tokenize, pos_tag
from nltk.chunk import RegexpParser
from nltk.tree import Tree

# Define grammar to identify phrases
grammar = r'''
    S: {<NP><VP>}                       # Sentence structure
    NP: {<DT>?<JJ>*<NN.*>}              # Noun Phrase
    VP: {<VB.*><NP|PP|CLAUSE|JJ>+}      # Verb Phrase
    PP: {<IN><NP>}                      # Prepositional Phrase
'''

chunk_parser = RegexpParser(grammar)

# Convert the tree into a simplified list of (label, tokens) tuples
# For subtrees (NP, VP, etc.), collect the phrase label and tokens
# For unchunked tokens, label them as "O" for Outside

def simplifyChunks(tree):
    simplified = []

    for subtree in tree:
        if isinstance(subtree, Tree):
            label = subtree.label()
            tokens = []
            for child in subtree:
                if isinstance(child, Tree):
                    tokens.extend(child.leaves())
                else:
                    tokens.append(child)
            simplified.append((label, tokens))
        else:
            simplified.append(("O", [subtree]))

    return simplified

# Tokenize, tag, chunk, and simplify the sentence

def getChunks(sentence):
    tokens = word_tokenize(sentence)
    tags = pos_tag(tokens)
    chunk_tree = chunk_parser.parse(tags)
    return simplifyChunks(chunk_tree)

sentence = "The quick brown fox jumped over the lazy dog"
print(getChunks(sentence))
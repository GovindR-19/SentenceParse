import string
from nltk import word_tokenize, pos_tag
from nltk.chunk import RegexpParser
from nltk.tree import Tree

# Define grammar to identify phrase components
grammar = r'''
        S:  {<NP><VP>}                    
        NP: {<DT>?<JJ.*>*<NN.*>+}         
        VP: {<VB.*><NP|PP|ADJP|RB.*>*}    
        PP: {<IN><NP>}                   
'''

chunk_parser = RegexpParser(grammar)

## Method to generate the Syntactic Tree
def generateTree(tree):
    simplified = []
    ## For loop to build Syntactic Tree
    ## Tokens are assigned Labels
    for subtree in tree:
        if isinstance(subtree, Tree):
            label = subtree.label()
            tokens = []
            ## Finding subtrees and appending 
            for child in subtree:
                if isinstance(child, Tree):
                    tokens.extend(child.leaves())
                else:
                    tokens.append(child)
            simplified.append((label, tokens))
        else:
            simplified.append(("O", [subtree]))

    return simplified

## Tokenising a sentence and adding tags
def getChunks(sentence):
    tokens = word_tokenize(sentence)                                ## Tokenizing sentence
    tokens = [t for t in tokens if t not in string.punctuation]     ## Filtering out .,?!
    tags = pos_tag(tokens)                                          ## Assigning tags to tokens
    chunk_tree = chunk_parser.parse(tags)                           ## Further refining tags allocation
    return generateTree(chunk_tree)

sentence = "The quick brown fox jumped over the lazy dog"
print(getChunks(sentence))
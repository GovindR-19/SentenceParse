import nltk
from nltk import word_tokenize, pos_tag
from nltk.chunk import RegexpParser

def process_sentence(sentence):
    tokens = word_tokenize(sentence)
    pos_tags = pos_tag(tokens)

    grammar = r"""
        NP: {<DT|JJ|NN.*>+}             # Noun Phrase
        VP: {<VB.*><NP|PP|CLAUSE>+$}    # Verb Phrase
        PP: {<IN><NP>}                  # Prepositional Phrase
    """
    parser = RegexpParser(grammar)
    chunk_tree = parser.parse(pos_tags)

    print("\nParse Tree (Formatted):")
    chunk_tree.pretty_print()  # This will show each word on its own line

if __name__ == "__main__":
    sentence = input("Enter a sentence: ")
    process_sentence(sentence)

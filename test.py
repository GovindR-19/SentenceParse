from nltk import pos_tag, word_tokenize, ne_chunk

# # Only needed once to download required tokenizer models

# # Input text
# text = input("Enter a sentence or paragraph: ")
text = '''To bait fish withal; if it will feed nothing else,
it will feed my revenge.'''

# # Tokenize the input
tokens = word_tokenize(text)

tags = pos_tag(tokens)

tree = ne_chunk(tags)


print('\nword\t\ttag\n')
sentence = ""
for word, tag in tags:
   if(word not in ".,;"):
    print( f"{word}\t\t{tag}")
   
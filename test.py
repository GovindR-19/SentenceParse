from nltk import pos_tag, word_tokenize, ne_chunk

# # Only needed once to download required tokenizer models

# # Input text
# text = input("Enter a sentence or paragraph: ")
text = 'The quick brown fox saw the lazy dog sleeping.'

# # Tokenize the input
tokens = word_tokenize(text)

tags = pos_tag(tokens)

##Tree tags added
# tree = ne_chunk(tags)


print('\nword\t\ttag\n')
sentence = ""
for word, tag in tags:
   if(word not in ".,;"):
    print( f"{word}\t\t\t{tag}")
   
# print(tree)
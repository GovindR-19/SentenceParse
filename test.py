from nltk import pos_tag, word_tokenize, ne_chunk

# # Only needed once to download required tokenizer models

# # Input text
# text = input("Enter a sentence or paragraph: ")
text = "Did the quick brown fox jumped over the moon?"

# # Tokenize the input
tokens = word_tokenize(text)

tags = pos_tag(tokens)

tree = ne_chunk(tags)

tree.draw()

for word ,thingy in tags:
    
    if(thingy in "?.!;:"):
        thingy = "Punctuation"

    print(f'{thingy} : {word}')
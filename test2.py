from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, download

download('wordnet')

lemmatizer = WordNetLemmatizer()
text = "The cats are running in the gardens."
tokens = word_tokenize(text)
lemmas = [lemmatizer.lemmatize(token) for token in tokens]
print(lemmas)
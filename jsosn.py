import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
all_stopword=stopword.words('english')
all_stopwords = stopwords.append(',', '@')

with open('temp.json', 'r') as json_file:
    json_load = json.load(json_file)


for x in range(len(json_load)):
    text = json_load[x]["Source of Tweet"]
    text_tokens=word_tokenize(text,language="english",preserve_line=True)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
    print(tokens_without_sw)
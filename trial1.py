#import necessary libraries
import string 
import io
import random
import warnings
import numpy as np
#import ML libraries
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) 
nltk.download('punkt') 
nltk.download('wordnet') 
import warnings
warnings.filterwarnings('ignore')



#Reading in the corpus
with open('cr7.txt','r', encoding='utf8', errors ='ignore') as f:
    raw_text = f.read().lower()

#TOkenisation
sent_tokens = nltk.sent_tokenize(raw_text)
word_tokens = nltk.word_tokenize(raw_text)

# Preprocessing
lemmas = WordNetLemmatizer()

# Keyword Matching
igreets = ("hi", "hey", "hello", "greetings", "what's up", "sup", "good morning", "good eveining")
outgreets = ["hi", "hey","hi there", "hello"]

def lemmatizeTokens(tokens):
    return [lemmas.lemmatize(token) for token in tokens]

dictOfWords = dict((ord(punct), None) for punct in string.punctuation)

def normalizeLemma(text):
    return lemmatizeTokens(nltk.word_tokenize(text.lower().translate(dictOfWords)))

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in igreets:
            return random.choice(outgreets)


# Generating response
def response(user_input):
    amara_response=''
    sent_tokens.append(user_input)
    TfidfVec = TfidfVectorizer(tokenizer=normalizeLemma, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    values = cosine_similarity(tfidf[-1], tfidf)
    index=values.argsort()[0][-2]
    flat_vals = values.flatten()
    flat_vals.sort()
    req_tfidf = flat_vals[-2]
    if(req_tfidf!=0):
        amara_response = amara_response+sent_tokens[index]
        return amara_response
    else:
        amara_response=amara_response+"I did not comprehend your response. I am sorry!"
        return amara_response


flag=True
print("Amara: My name is Amara. I will try to answer your questions about XYZ. If you want to exit, type Bye!")
while(flag==True):
    user_input = input()
    user_input=user_input.lower()
    if(user_input=='bye'):
        flag=False
        print("Amara: Bye!")
    else:
        if(user_input=='thanks' or user_input=='thank you' ):
            flag=False
            print("Amara: You are welcome.")
        else:
            if(greeting(user_input)==None):
                print("Amara: ",end="")
                print(response(user_input))
                sent_tokens.remove(user_input)
            else:
                print("Amara: "+greeting(user_input))
                
          
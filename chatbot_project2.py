'''
James Anyabine(joa170000) and Mahathir Maxim(mhm180000)
CS 4395 HLT
Project 2 Chatbot
Date: Apirl 10, 2022
'''

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

#user class to save information about individual user
class User:
  def __init__(self, name, val):
    self.name = name
    self.likes = val

#Reading in the corpus
with open('elon.txt','r', encoding='utf8', errors ='ignore') as f:
    raw_text = f.read().lower()

#TOkenisation
sent_tokens = nltk.sent_tokenize(raw_text)
word_tokens = nltk.word_tokenize(raw_text)

# Preprocessing
lemmas = WordNetLemmatizer()

# Keyword Matching
igreets = ("hi", "hey", "hello", "greetings", "what's up", "sup", "good morning", "good eveining")
outgreets = ["Hi", "Hey","Hi there", "Hello"]
iFeels=("how are you", "how are you doing")
outFeels=["I am fine. Thanks for asking"]



def lemmatizeTokens(tokens):
    '''
    function for lemmatizing tokens
    Args:
        tokens: word tokens
    Returns:
        temmatized list of tokens
    '''
    return [lemmas.lemmatize(token) for token in tokens]

dictOfWords = dict((ord(punct), None) for punct in string.punctuation)

def normalizeLemma(text):
    '''
    function for normalizing text
    Args:
        text: raw text
    Returns:
        normalized text
    '''
    return lemmatizeTokens(nltk.word_tokenize(text.lower().translate(dictOfWords)))

def greeting(sentence):
    '''
    function to check if user response is greetings and response accordingly
    '''
    for word in sentence.split():
        if word.lower() in igreets: # check if user response contains greetings words
            return random.choice(outgreets)


# Generating response
def response(user_input):
    '''
    function for generating response from knowledge base based on user response using tf-idf and cosine similarity
    Args:
        user_input: user query
    Returns: 
        generated response from knowledgebase
    '''
    amara_response=''
    sent_tokens.append(user_input)
    TfidfVec = TfidfVectorizer(tokenizer=normalizeLemma, stop_words='english') #Sklearn tf-idf
    tfidf = TfidfVec.fit_transform(sent_tokens) #get tf-idf value for sent tokens
    values = cosine_similarity(tfidf[-1], tfidf) # get values based on cosine similarity
    index=values.argsort()[0][-2]
    flat_vals = values.flatten()
    flat_vals.sort()
    req_tfidf = flat_vals[-2]
    if(req_tfidf!=0): #when chatbot can find a response from the knowledgebase
        amara_response = amara_response+sent_tokens[index]
        return amara_response
    else: #when chatbot cannot find a response from the knowledgebase
        amara_response=amara_response+"I did not comprehend your response. I am sorry!"
        return amara_response


#this code block uses rules based approach and where it exceeds rules it calls the response function to get response
flag=True
users=[]
names=set()
exit= False
while exit==False:
    print("\n\n\n")
    print("Amara: My name is Amara. I will try to answer your questions about Elon Musk.")
    print("Amara: If you want to exit, type exit!")
    print("Amara: If you want to start a new session, type bye!")
    print("Amara: Before we begin can I know your name? (Please right your name only)")
    name=str(input())
    if(name=='bye'):
            flag=False
            print("Amara: Bye!")
            continue
    elif(name=='exit'):
            flag=False
            exit=True
            print("Amara: Bye!")
            continue
    if name in names:
        print("Amara: Nice to see you again", name)
    else:   
        print("Amara: Nice to meet you, ", name)
        names.add(name)
    print("Amara: Do you know about Elon Musk? (Please respond with yes/no only)")
    likes=input()
    if(likes=='bye'):
            flag=False
            print("Amara: Bye!")
            continue
    elif(likes=='exit'):
            flag=False
            exit=True
            print("Amara: Bye!")
            continue
            
    if likes.lower()=='yes':
        likes=True
    else:
        likes=False
    curr_user=User(name, likes) #create user object 
    users.append(curr_user) # add user object to user object list working as a user model
    print("Amara: Thank you", name, "Now tell me how can I help you?")
    while(flag==True):
        user_input = input()
        user_input=user_input.lower()
        if(user_input=='bye'):
            flag=False
            print("Amara: Bye!")
        elif(user_input=='exit'):
            flag=False
            exit=True
            print("Amara: Bye!")
        else:
            if(user_input=='thanks' or user_input=='thank you' ):
                print("Amara: You are welcome.")
            elif user_input=='how are you' or user_input=='how are you doing':
                print('I am doing fine. Thanks for asking.')
            else:
                if(greeting(user_input)==None): #if none applies call the response function to get response from knowledge base
                    print("Amara: ",end="")
                    print(response(user_input))
                    sent_tokens.remove(user_input)
                else:
                    print("Amara: "+greeting(user_input))
    flag=True
                
          
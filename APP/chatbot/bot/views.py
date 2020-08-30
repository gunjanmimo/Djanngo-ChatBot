from django.shortcuts import render
from django.http import HttpResponse
#! NLP model
# ? importing libraries
from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')


# ? get article
article = Article(
    'https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521')
article.download()
article.parse()
article.nlp()
corpus = article.text

# ? tokenization
text = corpus
sentence_list = nltk.sent_tokenize(text)


# ? function to return random greeting response
def greeting_response(text):
    text = text.lower()

    # bot greeting response
    bot_greetings = ['howdy', 'hi', 'hello', 'hola']
    # user greetings
    user_greetings = ['hi', 'hey', 'hello', 'greetings', 'wassup']

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)


def index_sort(a):
    length = len(a)
    list_index = list(range(0, length))

    x = a
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                # swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
        return list_index


# creating bot response
def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_score = cosine_similarity(cm[-1], cm)
    similarity_score_list = similarity_score.flatten()
    index = index_sort(similarity_score_list)
    index = index[1:]
    response_flag = 0

    j = 0
    for i in range(len(index)):
        if similarity_score_list[index[i]] > 0.0:
            bot_response = bot_response + " "+sentence_list[index[i]]
            response_flag = 1
            j = j+1
        if j > 2:
            break
    if response_flag == 0:
        bot_response = bot_response+" " + "I am soory, I don't understand "

    sentence_list.remove(user_input)

    return bot_response


# Create your views here.


def index(request):
    context = {'a': 'hello world'}
    return render(request, 'chat.html', context)


def getResponse(request):
    if request.method == 'POST':
        msg = request.POST.get('message')
    # start the chat
    print("Doc Bot: I am a doctor bot. I will answer your questions. If want to exit, type BYE")

    exit_list = ['exit', 'see you later', 'break', 'quit', 'bye']
    while(True):
        user_input = input()
        if user_input.lower() in exit_list:
            print("Doc BOt: Thank you for using me")
            break
        else:
            if greeting_response(user_input) != None:
                print("Doc Bot: "+greeting_response(user_input))
            else:
                print("Doc Bot: "+bot_response(user_input))

    context = {'a': msg}
    return render(request, 'chat.html', context)

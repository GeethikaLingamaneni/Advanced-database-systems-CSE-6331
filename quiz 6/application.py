import os
from flask import Flask,redirect,render_template,request
import random
import urllib
import datetime
import json
import pickle
import hashlib
import requests
import nltk
import csv
from nltk.corpus import stopwords
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
nltk.download('punkt')
nltk.download('stopwords')
# print(stopwords.words('english'))
from collections import Counter
import io



application = Flask(__name__)

def bi_grams():
     f=open("static/monster.txt", "r")
     if f.mode == 'r':
        contents =f.read()
        contents=contents.lower()
        en_stops = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
                   'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                     'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'.',"?", "!", ";", ":", "-", "''" , "(", ")" , "[","]" , "/" ,"<",">",",","''",'""','``','--','_']
        word_tokens = word_tokenize(contents)
        filtered_sentence = [w for w in word_tokens if not w in en_stops] 
        filtered_sentence = []
        text= ''
        for word in word_tokens: 
            if word not in en_stops:
                filtered_sentence.append(word)
                text = text + word + " "
        #text = "this is the good place this is great this is me."
        #demo text
        words = text.split()
        #Create your bigrams
        bgs = nltk.bigrams(words)
        #compute frequency distribution for all the bigrams in the text
        fdist = nltk.FreqDist(bgs)
        for k,v in fdist.items():
            print(k)
            print(v)
        return render_template('index.html', list1 = fdist.items())
def Al_sw():
     filtered_sentence1 = []
     text= ''
     f=open("static/Alamo.txt", "r",encoding='utf-8',errors='ignore')
     f1=open("static/SpanishStopWords.csv", "r",encoding='utf-8',errors='ignore')
     if f1.mode == 'r':
        contents1 =f1.read()
        contents1=contents1.lower()
        en_stops1 = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
                   'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                     'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'.',"?", "!", ";", ":", "-", "''" , "(", ")" , "[","]" , "/" ,"<",">",",","''",'""','``','--','_']
        word_tokens1 = word_tokenize(contents1)
        for word in word_tokens1: 
            if word not in en_stops1:
                filtered_sentence1.append(word)
        print(filtered_sentence1)
     if f.mode == 'r':
        contents =f.read()
        contents=contents.lower()
        word_tokens = word_tokenize(contents)
        filtered_sentence = []
        print(word_tokens)
        for word in word_tokens: 
            if word  in filtered_sentence1:
                filtered_sentence.append(word)
                text = text + word + " "
        return render_template('display.html', x=text)   
    
def Al_removesw():
     filtered_sentence1 = []
     text= ''
     myDict ={}
     f=open("static/Alamo.txt", "r",encoding='utf-8',errors='ignore')
     f1=open("static/SpanishStopWords.csv", "r",encoding='utf-8',errors='ignore')
     if f1.mode == 'r':
        contents1 =f1.read()
        contents1=contents1.lower()
        en_stops1 = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
                   'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                     'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'.',"?", "!", ";", ":", "-", "''" , "(", ")" , "[","]" , "/" ,"<",">",",","''",'""','``','--','_']
        word_tokens1 = word_tokenize(contents1)
        for word in word_tokens1: 
            if word not in en_stops1:
                filtered_sentence1.append(word)
     if f.mode == 'r':
        contents =f.read()
        contents=contents.lower()
        word_tokens = word_tokenize(contents)
        filtered_sentence = []
        for word in word_tokens: 
            if word  not in filtered_sentence1:
                filtered_sentence.append(word)
                text = text + word + " "
        for i,word in enumerate(word_tokens):
            if word in filtered_sentence1:
                myDict.update([(word_tokens[i-1],word_tokens[i+1])])
        return render_template('show.html', ba=myDict.items(), withoutsw = text )   
    
def find_author():
     f=open("static/monster.txt", "r",encoding='utf-8',errors='ignore')
     if f.mode == 'r':
        contents =f.read()
        contents=contents.lower()
        en_stops = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
                   'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                     'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'.',"?", "!", ";", ":", "-", "''" , "(", ")" , "[","]" , "/" ,"<",">",",","''",'""','``','--','_']
        word_tokens = word_tokenize(contents)
        filtered_sentence = [w for w in word_tokens if not w in en_stops] 
        filtered_sentence = []
        text= ''
        for word in word_tokens: 
            if word not in en_stops:
                filtered_sentence.append(word)
                text = text + word + " "
        #text = "this is the good place this is great this is me."
        #demo text
        words = text.split()
        #Create your bigrams
        bgs = nltk.bigrams(words)
        #compute frequency distribution for all the bigrams in the text
        fdist = nltk.FreqDist(bgs)
        for k,v in fdist.items():
            print(k)
            print(v)
        return render_template('index.html', list1 = fdist.items())

def most_common():
     f=open("static/monster.txt", "r",encoding='utf-8',errors='ignore')
     if f.mode == 'r':
        contents =f.read()
        contents=contents.lower()
        en_stops = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
                   'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                     'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'.',"?", "!", ";", ":", "-", "''" , "(", ")" , "[","]" , "/" ,"<",">",",","''",'""','``','--','_']
        word_tokens = word_tokenize(contents)
        filtered_sentence = [w for w in word_tokens if not w in en_stops] 
        filtered_sentence = []
        text= ''
        for word in word_tokens: 
            if word not in en_stops:
                filtered_sentence.append(word)
                text = text + word + " "
        words = text.split()
        counter = Counter(words)
        mf = counter.most_common(1)
        return render_template('index.html',x=mf)
    
def least_common():
     f=open("static/monster.txt", "r",encoding='utf-8',errors='ignore')
     if f.mode == 'r':
        contents =f.read()
        contents=contents.lower()
        en_stops = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
                   'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                     'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'.',"?", "!", ";", ":", "-", "''" , "(", ")" , "[","]" , "/" ,"<",">",",","''",'""','``','--','_']
        word_tokens = word_tokenize(contents)
        filtered_sentence = [w for w in word_tokens if not w in en_stops] 
        filtered_sentence = []
        text= ''
        for word in word_tokens: 
            if word not in en_stops:
                filtered_sentence.append(word)
                text = text + word + " "
        words = text.split()
        counter = Counter(words)
        mf = counter.most_common() 
        lc = mf[-1]
       # lc =  sorted_items[-1:]
        #print(lc)
        return render_template('index.html',y=lc)


def reading():
    f=io.open("static/monster.txt", "r",encoding='utf-8',errors='ignore')
    text= ''
    if f.mode == 'r':
        contents =f.read()
        contents=contents.lower()
        en_stops = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
                    'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                      'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'.',"?", "!", ";", ":", "-", "''" , "(", ")" , "[","]" , "/" ,"<",">",",","''",'""','``','--','_']
        word_tokens = word_tokenize(contents)
        filtered_sentence = [w for w in word_tokens if not w in en_stops] 
        filtered_sentence = []
        
        for word in word_tokens: 
            if word not in en_stops:
                filtered_sentence.append(word)
                text = text + word + " "
    return render_template('index.html',p=text)

def find_occurances(a=None):
    f=open("static/monster.txt", "r",encoding='utf-8',errors='ignore')
    wordre = {}
    if f.mode == 'r':
        contents =f.read()
        contents=contents.lower()
        print(contents)
        en_stops = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
                   'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                     'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'.',"?", "!", ";", ":", "-", "''" , "(", ")" , "[","]" , "/" ,"<",">",",","''",'""','``','--','_']
        word_tokens = word_tokenize(contents)
        filtered_sentence = [w for w in word_tokens if not w in en_stops] 
        filtered_sentence = []
        text= ''
        for word in word_tokens: 
            if word not in en_stops:
                filtered_sentence.append(word)
                text = text + word + " "
        words = text.split()
        counter = Counter(words)
        mf = counter.most_common() 
        gw = a.split()
        print(gw)
        #print(mf)
        for x in mf: 
            if x[0] in gw:
                wordre.update({(x[0],x[1])})
        print(wordre)
    return render_template('index.html',oc = wordre.items())

def find_occurances2(a=None):
    f1=open("static/monster.txt", "r",encoding='utf-8',errors='ignore')
    wordre = {}
    gw=[]
    if f1.mode == 'r':
        contents1 =f1.read()
        contents1=contents1.lower()
        en_stops1 = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
                   'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                     'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'.',"?", "!", ";", ":", "-", "''" , "(", ")" , "[","]" , "/" ,"<",">",",","''",'""','``','--','_']
        word_tokens1 = word_tokenize(contents1)
        filtered_sentence1 = [w for w in word_tokens1 if not w in en_stops1] 
        filtered_sentence1 = []
        text= ''
        for word in word_tokens1: 
            if word not in en_stops1:
                filtered_sentence1.append(word)
                text = text + word + " "
        words1 = text.split()
        counter1 = Counter(words1)
        mf1 = counter1.most_common(20) 
        for x in mf1:
            gw.append(x[0])      
    f=open("static/milton.txt", "r",encoding='utf-8',errors='ignore')
    wordre = {}
    if f.mode == 'r':
        contents =f.read()
        contents=contents.lower()
        print(contents)
        en_stops = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
                   'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                     'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'.',"?", "!", ";", ":", "-", "''" , "(", ")" , "[","]" , "/" ,"<",">",",","''",'""','``','--','_']
        word_tokens = word_tokenize(contents)
        filtered_sentence = [w for w in word_tokens if not w in en_stops] 
        filtered_sentence = []
        text= ''
        for word in word_tokens: 
            if word not in en_stops:
                filtered_sentence.append(word)
                text = text + word + " "
        words = text.split()
        counter = Counter(words)
        mf = counter.most_common() 
        for x in mf: 
            if x[0] in gw:
                wordre.update({(x[0],x[1])})
        print(wordre)
    return render_template('index.html',oc1 = wordre.items())

def closest_proximity(w1=None,w2=None):
    f=open("static/monster.txt", "r",encoding='utf-8',errors='ignore')
    wordre = {}
    if f.mode == 'r':
        contents =f.read()
        contents=contents.lower()
        en_stops = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
                   'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                     'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'.',"?", "!", ";", ":", "-", "''" , "(", ")" , "[","]" , "/" ,"<",">",",","''",'""','``','--','_']
        word_tokens = word_tokenize(contents)
        filtered_sentence = [w for w in word_tokens if not w in en_stops] 
        filtered_sentence = []
        text= ''
        for word in word_tokens: 
            if word not in en_stops:
                filtered_sentence.append(word)
                text = text + word + " "
        words = text.split()
        min_dist = len(words)+1 
        # traverse through the entire string 
        for index in range(len(words)): 
            if words[index] == w1: 
                for search in range(len(words)): 
                    if words[search] == w2:  
                        curr = abs(index - search) - 1; 
                        if curr < min_dist:
                            min_dist = curr
        print(min_dist)
    return render_template('index.html',mind = min_dist)

def nleast(n=None):
     filtered_sentence1 = []
     text= ''
     myDict ={}
    
     f=open("static/Alamo.txt", "r",encoding='utf-8',errors='ignore')
     f1=open("static/SpanishStopWords.csv", "r",encoding='utf-8',errors='ignore')
     if f1.mode == 'r':
        contents1 =f1.read()
        contents1=contents1.lower()
        en_stops1 = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
                   'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                     'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'.',"?", "!", ";", ":", "-", "''" , "(", ")" , "[","]" , "/" ,"<",">",",","''",'""','``','--','_']
        word_tokens1 = word_tokenize(contents1)
        for word in word_tokens1: 
            if word not in en_stops1:
                filtered_sentence1.append(word)
                text = text + word + " "
        words = text.split()
        counter = Counter(words)
        mf = counter.most_common() 
        l=mf[-int(n):]
        return render_template('dis.html', l=l)  
def wordinput():
    nouns=[]
    f=io.open("static/Grimm.txt", "r",encoding='utf-8',errors='ignore')
    if f.mode == 'r':
        contents =f.read()
        nltk_tokens = nltk.sent_tokenize(contents)
        sentences = nltk_tokens
        sent_list = []
        for sentence in sentences:
            x = word_tokenize(sentence)
            for i,z in enumerate(x):
                if i>0:
                  if z[0].isupper():
                      nouns.append(z)
        return render_template('sh.html',p=nouns)

def ad_nouns():
    nouns=[]
    mis=[]
    sev=[]
    flag = 0
    flag1 = 0
    f=io.open("static/Grimm.txt", "r",encoding='utf-8',errors='ignore')
    if f.mode == 'r':
        contents =f.read()
        nltk_tokens = nltk.sent_tokenize(contents)
        sentences = nltk_tokens
        sent_list = []
        for sentence in sentences:
            flag = 0
            flag1 = 0
            x = word_tokenize(sentence)
            for i in range(0,len(x)):
                
                if (i<len(x) and x[i][0:1].isupper() and x[i+1][0:1].isupper()):
                    flag=1
                if (i<len(x) and x[i][0:1].isupper() and x[i][0:1].isupper()):
                    flag1=1   
            if(flag==1):
                if sentence not in sev:
                    mis.append(sentence)
            if(flag1==1):
                if sentence not in mis:
                    sev.append(sentence)
    print(mis)
    print(sev)
    return render_template('x.html',mis =mis, sev=sev)

def number():
	f=io.open("static/SpanishEnglishFreq.csv", "r",encoding='utf-8',errors='ignore')
	if f.mode == 'r':
		contents =f.read()
		contents=contents.lower()
		nltk_tokens = nltk.sent_tokenize(contents)
		print(nltk_tokens)
		sentences = nltk_tokens
		search_keywords='''([0-9]+)'''
		sent_list = []
		for sentence in sentences:
			x = word_tokenize(sentence)
			for z in x:
				if z in search_keywords:
					sent_list.append(sentence)
					break
			print(sent_list)
			
	return render_template('punct.html',p=sent_list)

def checker(a=None):
    f=io.open("static/EnglishWordsMostFreq.csv", "r",encoding='utf-8',errors='ignore')
    gw=[]
    rw=[]
    if f.mode == 'r':
        contents =f.read()
        contents=contents.lower()
        c1 = word_tokenize(contents)
        text = a.split()
        for word in text:
            if word in c1:
                gw.append(word)
            else:
                rw.append(word)
    print(gw)
    print(rw)
    return render_template('display.html',rw=rw, gw=gw)

def checker_span(a=None):
    f=io.open("static/SpanishEnglishFreq.csv", "r",encoding='utf-8',errors='ignore')
    gw=[]
    rw=[]
    y=''
    p=''
    if f.mode == 'r':
        contents =f.read()
        contents=contents.lower()
        
        
        #print(nltk_tokens)
        d =  contents.split('\n')
        for j in d:
            if a in j:
                p=j
    
    z=p.split(',')
    return render_template('show.html',p=z)
    
def checker_eng(a=None):
    f=open("static/EnglishWordsMostFreq.csv", "r",encoding='utf-8',errors='ignore')
    gw=[]
    text=[]
    c=0
    if f.mode == 'r':
        contents =f.read()
        contents=contents.lower()
        c1 = word_tokenize(contents)
        for x in c1:
            c=0
            for i in range(0,len(x)):
                c=0
                for j in range(0,len(a)):
                    if(i==0 and j== 0 and x[i]==a[j]):
                        c=c+1
                        k=i-1
                        p=i-1
                        if(k==-1 and p== -1 and c>0 and c<len(a)):
                            gw.append(x)
        print(gw)
        return render_template('sh.html', gw=gw)
@application.route("/spell")
def spell():
    a = request.args.get('word','')
    return checker(a)

@application.route("/but1")
def spell1():
    a = request.args.get('b1','')
    return checker_span(a)

@application.route("/but2")
def spell2():
    a = request.args.get('b2','')
    return checker_eng(a)

@application.route("/num")
def nb():
	return number()

@application.route("/adj")
def ad():
	return ad_nouns()

@application.route("/wordi")
def winput():
	return wordinput()
@application.route("/s")
def readwrite():
	return reading()

@application.route("/nl")
def nl():
    a = request.args.get('n','')
    return nleast(a)

@application.route("/rem")
def rem():
	return Al_removesw()

@application.route("/al")
def mn():
	return Al_sw()
@application.route("/")
def readwrite1():
	return render_template('index.html')
@application.route("/cp")
def cp():
    a = request.args.get('w1','')
    b = request.args.get('w2','')
    return closest_proximity(a,b)

@application.route("/oc2")
def foc2():
	return find_occurances2()

@application.route("/c")
def c():
    return most_common()


@application.route("/lc")
def lc():
    return least_common()
@application.route("/bigr")
def bigr():
    return bi_grams()
@application.route("/oc")
def oc():
    a = request.args.get('st','')
    return find_occurances(a)



if __name__ == "__main__":
	application.run()
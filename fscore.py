#!/usr/bin/env python
# coding: utf-8

# In[11]:


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import json
import nltk


# In[32]:


def is_noun(postag):
    if(postag== "NN" or postag== "NNS" or postag== "NNP" or postag== "NNPS"):
        return True
    return False


# In[33]:


def is_adjective(postag):
    if(postag== "JJ" or postag== "JJS" or postag== "JJR"):
        return True
    return False


# In[34]:


def is_preposition(postag):
    if(postag== "IN"):
        return True
    return False


# In[35]:


def is_article(postag):
    if(postag== "DET"):
        return True
    return False


# In[36]:


def is_pronoun(postag):
    if(postag== "PRP" or postag== "PRP$" or postag== "WP" or postag== "WP$"):
        return True
    return False


# In[43]:


def is_verb(postag):
    if(postag== "VB" or postag== "VBD" or postag== "VBG" or postag== "VBN" or postag== "VBP" or postag== "VBZ"):
        return True
    return False


# In[38]:


def is_adverb(postag):
    if(postag== "RB" or postag== "RBS" or postag== "RBR" or postag== "WRB"):
        return True
    return False


# In[39]:


def is_interjection(postag):
    if(postag== "UH"):
        return True
    return False


# In[44]:


def get_score(text):
    sents= nltk.sent_tokenize(text)
    total= 0
    dictt= {}
    dictt['nouns']= 0
    dictt['adjectives']= 0
    dictt['prepositions']= 0
    dictt['articles']= 0
    dictt['pronouns']= 0
    dictt['verbs']= 0
    dictt['adverbs']= 0
    dictt['interjections']= 0
    for sent in sents:
        wordlist= nltk.word_tokenize(sent)
        total+= len(wordlist)
        tagged= nltk.pos_tag(wordlist)
        dictt['nouns']+= len([word for (word, pos) in tagged if(is_noun(pos))])
        dictt['adjectives']+= len([word for (word, pos) in tagged if(is_adjective(pos))])
        dictt['prepositions']+= len([word for (word, pos) in tagged if(is_preposition(pos))])
        dictt['articles']+= len([word for (word, pos) in tagged if(is_article(pos))])
        dictt['pronouns']+= len([word for (word, pos) in tagged if(is_pronoun(pos))])
        dictt['verbs']+= len([word for (word, pos) in tagged if(is_verb(pos))])
        dictt['adverbs']+= len([word for (word, pos) in tagged if(is_adverb(pos))])
        dictt['interjections']+= len([word for (word, pos) in tagged if(is_interjection(pos))])
    
    for key in dictt:
        dictt[key]= (dictt[key]/total)*100
    print (dictt)
    return fscore(dictt)


# In[45]:


def fscore(dictt):
    return (dictt['nouns'] + dictt['adjectives'] + dictt['prepositions'] + dictt['articles'] - dictt['pronouns'] 
            - dictt['verbs'] - dictt['adverbs'] - dictt['interjections'] + 100)/2


# In[48]:


def read_json(filename):
    loc= '/home/bansal/Downloads/' + filename + ".json"
    print (loc)
    scores= []
    count= 1
    for comment in open(loc, 'r'):
        text= json.loads(comment)['body']
        scores.append(get_score(text))
        print (count)
        count+= 1
    scores= np.array(scores)
    print ("Number of comments analyzed:" + str(len(scores)))
    print ("Mean F-Score of comments analyzed:" + str(np.mean(scores)))
    print ("Median F-Score of comments analyzed:" + str(np.median(scores)))
    outname= "/home/bansal/Documents/SML/SML/BTP/" + filename + "f" + '.txt'
    np.savetxt(outname, scores, newline=" ")
    print ("DONE!!!")
        
    


# In[47]:


print (get_score("I love shooting up the beautiful school."))


# In[49]:


read_json("results-science")


# In[ ]:





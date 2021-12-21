#!/usr/bin/env python
# coding: utf-8

# # CV Parsing and Summarization using Spacy 

# In[1]:


import spacy
import pickle
import random
import pandas as pd


# spaCy is regarded as the fastest NLP framework in Python, with single optimized functions for each of the NLP tasks it implements

# In[2]:


train_data = pickle.load(open('C:\\Users\\Meghna\\Desktop\\CV Ranking\\train_data.pkl','rb'))


# In[3]:


train_data[0]


# Each element of the training data is a tuple. The tuple consists of two parts. 
# 
# The first part is the complete textual data of the CV which is having a data type of string.
# The second part is a dictionary. The dictionary contains a list as the value and this is a list of tuples. The last element of each tuple is the LABEL

# In[4]:


type(train_data[0][0])


# In[5]:


type(train_data[0][1])


# The procedure that we are following to parse the CV is first convert all of the data in a CV in PDF format to text format. 
# 
# Next, we have to determine all of the requried entites in the CV(like College Name, Degree, Skills etc.) and the position from where that entitiy begins and ends.

# In[6]:


type(train_data)


# In[7]:


len(train_data)


# Named Entity Recognition (NER) is a standard NLP problem which involves spotting named entities (people, places, organizations etc.) from a chunk of text, and classifying them into a predefined set of categories.

# In[8]:


nlp = spacy.blank('en')

def train_model(train_data):
    if 'ner' not in nlp.pipe_names:     
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    
    #We are checking whether the NER is already present in the pipeline list or not
    #If not, we add it to the end of the pipeline list
    
    for _, annotation in train_data:
        #annotation is the second half of each training data tuple
        for ent in annotation['entities']:
            #Here, we are adding all the NER labels from the CV PDF into the dictionary
            #At position, index 2
            ner.add_label(ent[2])
     
    #Now we are going to train our model only on the NERs in our PDFs and will put all of the other NERs
    #into other_pipes list
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):     #Only train on required NERs
        optimizer = nlp.begin_training()
        
        for itn in range (10):                #We shall be performing training for 10 iterations
            print('Starting iteration ', itn)
            random.shuffle(train_data)        #By shuffling the training data
            losses = {}
            index = 0
            for text, annotations in train_data:
                try:
                    nlp.update([text],
                              [annotations],
                              drop=0.2,
                              sgd=optimizer,
                              losses=losses)
                except Exception as e:
                    pass
                    
            print(losses)


# In[9]:


train_model(train_data)


# In[10]:


#We will now save this trained NLP model to our local disk
nlp.to_disk('C:\\Users\\Meghna\\Desktop\\CV Ranking\\nlp_model')


# In[11]:


#Load trained model into spacy 
nlp_model = spacy.load('C:\\Users\\Meghna\\Desktop\\CV Ranking\\nlp_model')


# In[12]:


#Since we shuffled out training dataset, hence the first element is different now
train_data[0]


# Now, it's not a good idea to test our model on training data, but still lets see whether our model is working correctly or not by applying the model on a training dataset data.
# 
# So, we'll only be pasing the text to our model and check if we are getting the corresponding entities or not.

# In[13]:


doc = nlp_model(train_data[0][0])
for ent in doc.ents:
    print(f'{ent.label_.upper():{30}}-{ent.text}')


# Now, lets test the model on a random CV PDF file.

# So, first we need to extract the data from the PDF and then pass it through the model to get classification of text into different entites

# In[14]:


#!pip install PyMuPDF


# In[15]:


import sys, fitz
fname = 'C:\\Users\\Meghna\\Desktop\\CV Ranking\\Alice Clark CV.pdf'
doc = fitz.open(fname)
text = ""
for page in doc:
    text = text + str(page.get_text())
    
text


# In[16]:


print(text)


# As we can see, there are many special characters and new lines, so we need to remove these extra characters and obtain clean data. We'll do that as follows:

# In[17]:


clean_text = " ".join(text.split('\n'))
print(clean_text)


# Now, we'll test our model on this cleaned and processed text.

# In[18]:


doc = nlp_model(clean_text)
for ent in doc.ents:
    print(f'{ent.label_.upper():{30}}-{ent.text}')


# Let's test the model on another CV PDF.

# In[19]:


import sys, fitz
fname = 'C:\\Users\\Meghna\\Desktop\\CV Ranking\\Smith Resume.pdf'
doc = fitz.open(fname)
text = ""
for page in doc:
    text = text + str(page.get_text())
    
clean_text = " ".join(text.split('\n'))
print(clean_text)


# In[20]:


doc = nlp_model(clean_text)
for ent in doc.ents:
    print(f'{ent.label_.upper():{30}}-{ent.text}')


# Clearly, our model works and is efficiently able to extract all of the relevant information from the PDF CVs

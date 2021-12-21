#!/usr/bin/env python
# coding: utf-8

# # CV Dataset Creation using Parsed and Summarized CVs

# Through this module, we'll be using the NLP model that we created in the previous module to create a dataset for all the CVs that our system will receive thorough the candidates which will further be ranked according to the requirements of the Recruiter.

# In[1]:


import spacy
import pickle
import random
import pandas as pd


# In[2]:


Name=[]
Location=[]
Email_Address=[]
Degree=[]
College_Name=[]
Skills=[]
Designation=[]


# In[3]:


train_data = pickle.load(open('C:\\Users\\Meghna\\Desktop\\CV Ranking\\train_data.pkl','rb'))


# In[4]:


nlp_model = spacy.load('C:\\Users\\Meghna\\Desktop\\CV Ranking\\nlp_model')


# In[5]:


for x in range(200):
    doc = nlp_model(train_data[x][0])
    for ent in doc.ents:

        if(ent.label_ == 'Name'):
            Name.append(ent.text)
        elif(ent.label_ == 'Location'):
            Location.append(ent.text)
        elif(ent.label_ == 'Email Address'):
            Email_Address.append(ent.text)
        elif(ent.label_ == 'Degree'):
            Degree.append(ent.text)
        elif(ent.label_ == 'College Name'):
            College_Name.append(ent.text)
        elif(ent.label_ == 'Skills'):
            Skills.append(ent.text)
        elif(ent.label_ == 'Designation'):
            Designation.append(ent.text)


# In[6]:


df = pd.DataFrame(list(zip(Name,Location,Email_Address,Degree,College_Name,Skills,Designation)),
                  columns =['Name', 'Location','Email Address','Degree','College Name','Skills','Applied Role'])
df


# Now, we'll be saving this dataset to our local disk as follows:

# In[7]:


#Saving the dataframe
df.to_csv('CV_DataFrame.csv')


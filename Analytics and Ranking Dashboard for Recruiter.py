#!/usr/bin/env python
# coding: utf-8

# # Analytics Dashboard for Recruiter using Matplotlib

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import string


# In[2]:


import dash
from dash import dash_table as dt
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


# In[3]:


df = pd.read_csv('CV_Dataframe.csv')


# In[4]:


df.rename(columns = {'Unnamed: 0':'ID'}, inplace = True)


# In[5]:


df


# ### Cleaning and Processing the Dataset

# In[6]:


df['Applied Role'] = df['Applied Role'].str.title()
df['Applied Role']  = df['Applied Role'].str.strip()


# In[7]:


df['Applied Role'] = df['Applied Role'].str.replace('Senior', '')
df['Applied Role'] = df['Applied Role'].str.replace('Associate', '')
df['Applied Role'] = df['Applied Role'].str.replace('Systems Engineer', 'System Engineer')
df['Applied Role'] = df['Applied Role'].str.replace('Software Development', 'Software')


# In[8]:


df.loc[df['Applied Role'].str.contains('Developer', case=False), 'Applied Role'] = 'Developer'
df.loc[df['Applied Role'].str.contains('Consultant', case=False), 'Applied Role'] = 'Consultant'
df.loc[df['Applied Role'].str.contains('Automation', case=False), 'Applied Role'] = 'Automation'
df.loc[df['Applied Role'].str.contains('Analyst', case=False), 'Applied Role'] = 'Analyst'


# In[9]:


desig_count = df['Applied Role'].value_counts()
desig_count[:5]


# In[10]:


loc_count = df['Location'].value_counts()
loc_count[:19]


# ### Visulaizing the Dataset and Creating Dashboard

# In[11]:


# Creating the bar plot
fig = plt.figure(figsize =(20, 7))
plt.bar(desig_count.index[:5], desig_count.values[:5], color ='maroon',width = 0.3)
 
plt.xlabel("Designation")
plt.ylabel("Number of Applicants")
plt.title("Number of Applications for Different Roles")
plt.xticks(rotation=45)
plt.show()


# In[12]:


fig,ax = plt.subplots(figsize =(10, 7))
plt.pie(loc_count[:10].values, labels = loc_count[:10].index, autopct='%1.1f%%')
plt.show()


# ### Ranking and Sorting the CVs based on Requirement

# ##### Based on Role Available

# In[13]:


role_requirement = "Analyst"
required_df = df[df['Applied Role'] == role_requirement]
not_required_df = df[df['Applied Role'] != role_requirement]


# In[14]:


final_ranked_df = pd.concat([required_df,not_required_df], axis=0)


# In[15]:


final_ranked_df


# ##### Based on Location Available

# In[16]:


location_requirement = "Pune"
required_df = df[df['Location'] == location_requirement]
not_required_df = df[df['Location'] != location_requirement]


# In[17]:


final_ranked_df = pd.concat([required_df,not_required_df], axis=0)
final_ranked_df


# ### Creating Ranking Dashboard

# In[18]:


applied_role_df = df['Applied Role'].value_counts()
applied_role_df[:10]


# In[19]:


location_df = df['Location'].value_counts()
location_df[:10]


# In[ ]:


app = dash.Dash(__name__)


# In[ ]:


app.layout = html.Div([
    
    html.Div(children=[
        
            html.H1(children='RANKING DASHBOARD'), 
            html.Div(children='CV Screening and Analysis Recruiter Dashboard')],
            style={'textAlign': 'center','backgroundColor':'#355c7d','color': 'white','font-family':['Open Sans','sans-serif'], 
                   'font-style': ['italic'],'padding-top':'20px','padding-bottom':'40px','fontSize':17,'margin-bottom':'70px'}
            ),
    

    #This is the second row of the dashboard
    html.Div(children=[
            
            
            html.Div(children=[
                html.P('SELECT REQUIRED FEATURES ', style={'color':'white','textAlign': 'center','fontSize':'25px','font-style': ['bold']}),
                html.Br(),   
                
                html.P('SELECT LOCATION: ', style={'color':'white'}),
                dcc.Dropdown(
                        id='location_dropdown',
                        multi=False,
                        clearable=True,
                        value="Pune",
                        placeholder="Select Location:",
                        options=[{'label':c, 'value':c} for c in (location_df.index)]),
                html.Br(),
                html.Br(),
                html.Br(),
                
                html.P('SELECT DESIRED ROLE: ', style={'color':'white'}),
                dcc.Dropdown(
                        id='role_dropdown',
                        multi=False,
                        clearable=True,
                        value='Consultant',
                        placeholder="Select Role:",
                        options=[{'label':c, 'value':c} for c in (applied_role_df.index)]),
                html.Br(),
        
                ],
                style={'display':'inline-block','textAlign': 'left','backgroundColor': '#2D2D2D','color': 'black',
                        'margin-left':'25px','margin-right':'25px','width':'30%','border-radius':'5px',
                        'box-shadow':'2px 2px 2px #1f2c56','padding':'25px'}
            ),
        
        html.Div([
        
        dt.DataTable
    (
        id='cv_table',
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i, "deletable":False, "selectable":False} for i in ['ID','Name','Location','Email Address','Applied Role']],
        page_size=13
    )],
                style={'width':'70%','margin-right':'30x'}
        
    )  
        ], 

            style={'display':'flex'}
        )
])


# In[ ]:


@app.callback(
    Output('cv_table', 'data'),
    [Input('location_dropdown', 'value')]
)

def update_rows(selected_value):
    required_df = df[df['Location'] == (selected_value)]
    return required_df.to_dict('records')


# In[ ]:


if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:





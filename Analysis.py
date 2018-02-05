
# coding: utf-8

# In[140]:

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from ggplot import *
import time
import configparser
import requests
import os
import json
import urllib

sns.set_palette("GnBu_d")
sns.set_style('whitegrid')

# import hypertools as hyp
get_ipython().magic('matplotlib inline')


# In[117]:

def get_api_call_for_section(query):
    config = configparser.ConfigParser()
    config.read('config/config.cfg')
    BASE_URL = config.get('GUARDIAN', 'BASE_URL')
    API_KEY = config.get('GUARDIAN', 'API_KEY')

    # url_string = BASE_URL + 'search/v2/articlesearch.json?&fq=section_name:"' + section + '"&sort=newest&api-key=' + API_KEY
    url_string = BASE_URL + 'search?q=' + query + '&page-size=200&show-fields=headline,body,shorturl&api-key=' + API_KEY
    return url_string


# In[118]:

print('main code')
url_string = get_api_call_for_section('Einstein')
print('make call to ', url_string)
    
req = requests.get(url_string)
data = req.json()
with open('data.txt', 'w') as outfile:
    json.dump(data, outfile, indent=2, sort_keys=True)


# In[119]:

with open('data.txt', 'r') as f:
     data = json.load(f)
    


# In[120]:

search_results = data['response']['results']


# In[121]:

search_results_df = pd.DataFrame(search_results)
search_results_df.info()
search_results_df.head()


# In[144]:

g = sns.countplot(search_results_df['sectionName'], palette='GnBu_d')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('plots/plot1.png')


# In[154]:

# format = lambda x: str(x).split('T')[0]
def format(x):
    split = str(x).split('-')
    return split[0] + '-' + split[1]
search_results_df['date'] = search_results_df['webPublicationDate'].map(format)
search_results_df.head()

search_results_df = search_results_df.sort_values('date', ascending=True)



# sns.countplot(search_results_df['date'], palette='GnBu_d')
# plt.xticks(rotation=90)


# plt.savefig('plots/plot2.png')


# In[151]:

dates = search_results_df['date'].unique()

origin = dates[0].split("-")
origin
date_count = []
for date in dates:
    date_df = search_results_df[search_results_df['date'] == date]
    split_date = date.split("-")
    
    count = len(date_df)
    months = (int(split_date[0]) - int(origin[0]))*12 + int(split_date[1]) - int(origin[1])
    date_count.append({'date': date, 'count': count, 'months': months})
    
date_count = pd.DataFrame(date_count)
date_count.head()


# In[153]:

sns.regplot('count', 'months', date_count)
plt.savefig('plots/plot2.png')


# ## arXiv APi

# In[95]:

import xml.etree.ElementTree as ET

arxivUrl = 'http://export.arxiv.org/api/query?search_query=all:Einstein'

data = urllib.request.urlopen(arxivUrl).read()
with open('arxiv.xml', 'wb') as outfile:
    outfile.write(data)


# In[ ]:




# ## Wikipedia

# In[101]:

articles = pd.read_csv('/Volumes/Porsche/data/articles.csv')


# In[102]:

articles.head()


# In[ ]:




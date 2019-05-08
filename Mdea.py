#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from logger import Logger


# In[2]:


logger = Logger(show = True, html_output = True, config_file = "config.txt")

logger.log("Reading transactions file...")
df = pd.read_csv(logger.get_data_file(logger.config_dict['DATA_FILE']))
logger.log("Finish reading {} rows".format(df.shape[0]), show_time = True)


# In[3]:


df.head()
crt_size = df.shape[0]


# In[4]:


df['mail_id'] = df['mail_id'].str.replace('email','')
df.drop(df[df.mail_id == "NA"].index, inplace=True)
df['mail_id'] = pd.to_numeric(df['mail_id'])
logger.log("Dropping NA in email id {}".format(crt_size - df.shape[0]))
crt_size = df.shape[0]

df['ip_id']   = df['ip_id'].str.replace('ip','')
df.drop(df[df.ip_id == "NA"].index, inplace=True)
df['ip_id'] = pd.to_numeric(df['mail_id'])
logger.log("Dropping NA in ip id {}".format(crt_size - df.shape[0]))
crt_size = df.shape[0]

df['card_id'] = df['card_id'].str.replace('card','')
df.drop(df[df.card_id == "NA"].index, inplace=True)
df['card_id'] = pd.to_numeric(df['mail_id'])
logger.log("Dropping NA in card id {}".format(crt_size - df.shape[0]))
crt_size = df.shape[0]


# In[5]:


df.drop(df[df.simple_journal == "Refused"].index, inplace=True)
logger.log("Dropping REFUSED transaction {}".format(crt_size - df.shape[0]))
crt_size = df.shape[0] 


# In[6]:


logger.log("Number of NaNs per column:")
df.isna().sum()


# In[7]:


logger.log("Few examples of NaNs rows:")
df[df.isna().any(axis=1)].head()


# In[8]:


(df[df['cardverificationcodesupplied'].isna()].simple_journal == "Chargeback").sum()


# In[9]:


df.dropna(axis = 0, inplace = True)
logger.log("Drop the other NaNs {}".format(crt_size - df.shape[0]))
crt_size = df.shape[0]


# In[10]:


logger.log("Currencies are {}".format(np.unique(df.currencycode.values)))


# In[11]:


df['bookingdate']  = pd.to_datetime(df['bookingdate'])
df['creationdate'] = pd.to_datetime(df['creationdate'])
df = df.infer_objects()


# In[12]:


df.dtypes


# In[13]:


df.creationdate.head()


# In[14]:


df.sort_values('creationdate', inplace = True)


# In[15]:


df.head()


# In[16]:


df.tail()


# In[17]:


df.reset_index(drop = True, inplace = True)


# In[18]:


conversion = {'AUD': 0.699165, 'GBP': 1.31061, 'MXN': 0.222776586, 'NZD': 0.66152, 'SEK': 0.104405}

df['amount'] = df.apply(lambda e: e['amount'] * conversion[e['currencycode']], axis=1)


# In[19]:


df.head()


# In[20]:


df.tail()


# In[21]:


df.drop(["txid", "bookingdate"], inplace = True, axis = 1)
df.replace({'simple_journal': {"Settled": 0, "Chargeback": 1}}, inplace = True)

columns = ["creationdate", "card_id", "mail_id", "ip_id", "issuercountrycode", "txvariantcode", 
           "bin", "shoppercountrycode", "shopperinteraction", "cardverificationcodesupplied", 
           "cvcresponsecode", "accountcode", "amount", "currencycode", "simple_journal"]

df = df[columns]
df.rename(columns = {'simple_journal': 'label'}, inplace = True)


# In[22]:


df.mail_id = pd.Categorical(df.mail_id).codes
df.ip_id = pd.Categorical(df.ip_id).codes
df.card_id = pd.Categorical(df.card_id).codes


# In[23]:


df.head()


# In[24]:


df.columns


# In[25]:


numeric_df = df[['amount', 'label', 'cardverificationcodesupplied']]


# In[26]:


# from plot_utils import create_heat_map


# In[27]:


#corr = numeric_df.corr()
#corr
# create_heat_map('', numeric_df, '', logger)


# In[28]:


#from collections import Counter

#occ = Counter(df.card_id.values)


# In[29]:


from card_tracker import extract_feature

a = df[0:500]
_hash = {}

features = a.apply(lambda e: extract_feature(e, _hash), axis=1)


# In[30]:


from collections import Counter

occ = Counter(df.card_id.values)

occ.most_common()


# In[33]:


v = df.loc[df['card_id'] == 122956]


# In[34]:


v


# In[56]:


# v.values.to_list()


# In[35]:


_hash = {}

features = v.apply(lambda e: extract_feature(e, _hash), axis=1)


# In[51]:


a = features.to_list()
len(a[-1])


# In[54]:


# f = pd.DataFrame(features)

pd.DataFrame(features.to_list(), columns =[
        "Txn amount over month",
        "Average over 3 months",
        "Average daily over month",
        "Amount same day",
        "Number same day",
        "Amount currency type over month",
        "Number currency type over month",
        "Amount country type over month",
        "Number country type over month",
    ])
#vezi ca acu :) thx


# In[44]:


# In[ ]:





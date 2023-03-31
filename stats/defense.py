#!/usr/bin/env python
# coding: utf-8

# In[180]:


import pandas as pd
import matplotlib.pyplot as plt
from frames import games, info, events


# In[181]:


plays = games.query('type == "play" & event != "NP"')


# In[182]:


plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', 'year']


# In[183]:


pa = plays.loc[plays['player'].shift() != plays['player'],['year', 'game_id', 'inning', 'team','player']]


# In[184]:


pa = pa.groupby(['year', 'game_id', 'team']).size().reset_index(name="PA")
events.head()


# In[185]:


events = events.set_index(['year', 'game_id', 'team', 'event_type'])
events.head()


# In[186]:


events = events.unstack().fillna(0).reset_index()
events.head()


# In[187]:


events.columns = events.columns.droplevel()


# In[188]:


events.columns =['year', 'game_id', 'team', 'BB', 'E', 'H', 'HBP', 'HR', 'ROE', 'SO']


# In[189]:


events = events.rename_axis(None)


# In[190]:


events.head()


# In[191]:


events_plus_pa = pd.merge(events,pa,how="outer", left_on=['year', 'game_id','team'],right_on =['year', 'game_id','team'])


# In[193]:


defense = pd.merge(events_plus_pa,info)


# In[198]:


defense.loc[:, 'DER'] = 1 - ((defense['H'] + defense['ROE']) / (defense['PA']-defense['BB']- defense['SO']- defense['HBP']  - defense['HR'] ))


# In[200]:


defense.loc[:,'year']=pd.to_numeric(defense.loc[:,'year'])


# In[210]:


der = defense.loc[defense['year'] >=  1978,['year', 'defense','DER']]


# In[211]:


der.plot(x="year",y="DER",x_compat=True,xticks=range(1978, 2018, 4),rot=45)
plt.show()


# In[ ]:





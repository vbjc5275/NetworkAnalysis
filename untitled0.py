# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 09:18:08 2020

@author: Jerry
"""
from collections import defaultdict,deque
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import pandas as pd
#%%
friendships = [("郭靖","黃蓉"),("郭靖","楊康"),("郭靖","洪七公"),("郭靖","楊過"),
               ("郭靖","周伯通"),("郭靖","郭嘯天"),("郭靖","李萍"),
               ("黃蓉","黃藥師"),("黃蓉","洪七公"),("楊康","楊鐵心"),("楊康","歐陽鋒"),
               ("楊康","穆念慈"),("楊過","小龍女"),("周伯通","王重陽"),
               ("王重陽","丘處機"),("李萍","郭嘯天")]
#%%
#degree centrality

#計算好友數量
def degree_centrality(friendships):
    user_friend_count = defaultdict(int)
    for friendship in friendships:
        user_id, friend_id = friendship
        user_friend_count[user_id] += 1
        user_friend_count[friend_id] += 1
    return user_friend_count

def standardize(user_friend_count):
    #標準化-除以(n-1)(n-2)
    total_count = sum(user_friend_count.values())
    return {user:count/((total_count-1)*(total_count-2)) for user,count in user_friend_count.items()}

user_friend_count = degree_centrality(friendships)
user_friend_count_after_standardization = standardize(user_friend_count)

#make it readable
df = pd.DataFrame.from_dict(user_friend_count.items())
df.insert(2,"degree centrality(std)",user_friend_count_after_standardization.values())
df.columns = ["人物","degree centrality","degree centrality(std)"]
#%%

def construct_user_friends(friendships):
    """
    #Returns:
        key:userId
        value:friends list
    """
    user = defaultdict(list)
    for friendship in friendships:
        user_id, friend_id = friendship
        user[user_id].append(friend_id)
        user[friend_id].append(user_id)
    return user

def shortest_paths_from(from_user):
    shortest_paths = {}
    for friend_id in user[from_user]:
        shortest_paths[friend_id] = [from_user,friend_id]
    
    visited  = deque() #(節點路徑,該節點ID)
    for friend_id in user[from_user]:
        visited.append(([from_user,friend_id],friend_id))
        
    while visited:
        path,fri_id, = visited.popleft()
        user_friends = [fre for fre in user[fri_id] if fre not in shortest_paths and fre!=from_user]
        for fri_id in user_friends:
            cur_path = path[:]
            cur_path.append(fri_id)
            if fri_id not in shortest_paths:
                shortest_paths[fri_id] = cur_path
            visited.append((cur_path,fri_id))
    return shortest_paths

user = construct_user_friends(friendships)
shortest_paths_from("郭靖")   
for user in users:
    user["shortest_paths"] = shortest_paths_from(user)
#%% plot

#plt.rcParams['font.sans-serif'] = ['Source Han Sans TW']

def draw_basic_network_graph(from_,to):
    df = pd.DataFrame({ 'from':from_, 'to':to})
    G = nx.from_pandas_edgelist(df, 'from', "to")
    plt.figure(figsize=(8,8)) 
    nx.draw(G, with_labels=True, node_size=3500, font_size=20, font_family='Source Han Sans TW',font_color="yellow", font_weight="bold")
    plt.show()
    
from_ = [fre[0] for fre in friendships]
to = [fre[1] for fre in friendships]
draw_basic_network_graph(from_,to)

plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
import matplotlib
avail_font_names = [f.name for f in matplotlib.font_manager.fontManager.ttflist]

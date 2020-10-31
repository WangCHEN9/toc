# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 08:42:17 2020

@author: chenwang
"""

import re
import pandas as pd
import numpy as np

def ColumnValueCount(df,name):
    ## this function returns value count for cetain column
    Value_count = df[name].value_counts().to_frame().count(axis='rows').iloc[0]
    return Value_count

def FindColumn(df,keyword = 'latch',nb_col=1):
    
    for group in keyword:
        regex = r'^'
        for key in group:
            regex += r'(?=.*\b'+key+r'\b)'
            
            # regex = r'.*'+key+'.*'
        regex += r'.*$'
        
    
        ## this function returns latch force column name
        LatchForce_List = [z.group() for column in df.columns for z in [re.match(regex, column, re.I)] if z] ##Get all latch force into list
        
        if len(LatchForce_List)>=nb_col:
            counts_dic = {}
            for item in LatchForce_List:
                counts_dic[item] = ColumnValueCount(df,item)
            counts_dic_sorted = {k: v for k, v in sorted(counts_dic.items(),reverse = True, key=lambda item: item[1])} # sort dictionary by value

            FoundColumnName = list(counts_dic_sorted.keys())[:nb_col]
            RemovedCounts_list = [key for key in list(counts_dic_sorted.keys()) if key not in FoundColumnName]
            break
        else:
            FoundColumnName,RemovedCounts_list = False, False
    
    return FoundColumnName,RemovedCounts_list
    

def GetIssueRunid(df,RemovedCounts_list):
    ## this function returns Issue run ids (whose criteria name is not correct)
    Idlist = np.empty(shape=(1),dtype='str_')
    for Issue_run in RemovedCounts_list:
        Issue_run_index = df[df[Issue_run].notnull()].index.tolist()
        print(Issue_run_index)
        temp = df[df.index.isin(Issue_run_index)]
        print("temp1:\n",temp)
        temp = temp.iloc[:,0].values.tolist()
        print("temp2:\n",temp)
        
        np_temp = np.asarray(temp).flatten()
        Idlist = np.append(Idlist,np_temp)
    Idlist_all = np.delete(Idlist,0)
    Idlist_unique = np.unique(Idlist_all)
    return Idlist_unique


# function to get column name
def get_found_column(dataframe, keyword, nb_col = 1):
    found_column_name,RemovedCounts_list = FindColumn(dataframe,keyword, nb_col)
    if not found_column_name:
        msg = 'Keyword '+str(keyword)+' not found!'
        print(msg)
        return False
    Issue_runs = GetIssueRunid(dataframe,RemovedCounts_list)
    if(len(Issue_runs)==0):
        msg = "Keyword "+str(keyword)+' successfully matched'
        print(msg)
        pass
    else:
        msg = str(Issue_runs)+ ' have own "'+str(keyword)+'" column name compare to others, please correct it in THC setting'
        print(msg)
    return found_column_name 


# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np


# In[2]:

def maze_summary(dataframe, category):
    '''
    Calculate the means and standard deviations of certain categories in the dataframe.
    dataframe: data table, pandas dataframe
    category: user specified categories for calculation, python list
    '''
    maze_list = dataframe['maze'].unique().tolist()
    mode_list = dataframe['mode'].unique().tolist()
    summary_mean = pd.DataFrame()
    summary_std = pd.DataFrame()
    for maze in maze_list:
        for mode in mode_list:
            data = dataframe[(dataframe['maze'] == maze) & (dataframe['mode'] == mode)][category]
            data_mean = np.around(data.mean().values, decimals = 1).tolist()
            data_std = np.around(data.std().values, decimals = 1).tolist()
            summary_mean = summary_mean.append([[maze, mode] + data_mean], ignore_index = True)
            summary_std = summary_std.append([[maze, mode] + data_std], ignore_index = True)
    return (summary_mean, summary_std)


# In[3]:

def file_process(file_list):
    '''
    Process files for maze_summary.
    file_list: file name list, python list
    '''
    summary_mean = pd.DataFrame()
    summary_std = pd.DataFrame()
    for file in file_list:
        dataframe = pd.read_csv(file, sep = ',')
        category = dataframe.columns.values.tolist()[2:]
        summary = maze_summary(dataframe = dataframe, category = category)
        summary_mean = summary_mean.append(summary[0], ignore_index = True)
        summary_std = summary_std.append(summary[1], ignore_index = True)
    return (summary_mean, summary_std)


# In[4]:

file_list = ['test_result_maze_01.csv', 'test_result_maze_02.csv', 'test_result_maze_03.csv']


# In[5]:

column_names = ['Maze', 'Mode', 'Time Steps in First Run', 'Path Length in First Run', 
                'Time Steps in Second Run', 'Path Length in Second Run', 'Coverage', 'Score']


# In[6]:

summary = file_process(file_list = file_list)
summary_mean = summary[0]
summary_std = summary[1]


# In[7]:

summary_mean.columns = column_names
summary_std.columns = column_names


# In[8]:

summary_mean


# In[9]:

summary_std


# In[10]:

summary_mean.to_csv('summary_mean.csv', sep = ',', index = False)
summary_std.to_csv('summary_std.csv', sep = ',', index = False)


import os
import json
import re
import time
import pandas as pd
import numpy as np
from collections import Counter


def add_stateID(res, id_file='../locInfo/state_ID.csv'):
    '''
    Add a column for state ID to results
    '''
    id_state = np.genfromtxt(id_file, dtype='str', delimiter=',')
    state_id_dict = {item[1].lower(): item[0].lower() for item in id_state}

    result = pd.read_csv(res, sep=',', header=0)
    result['id'] = 0
    for i in range(result.shape[0]):
        result.at[i, 'id'] = int(state_id_dict[result.at[i, 'state'].lower()])

    result.to_csv(path_or_buf=res, sep=',', header=True, index=False, \
                  columns=['id', 'state', 'disease', 'count', 'SI_index'], index_label=None)

def add_percentage(res):
    '''
    Add a column for percentage of disease to results
    '''
    result = pd.read_csv(res, sep=',', header=0)
    states = set(result['state'].values)
    state_count_dict = {item: 0 for item in states}

    for i in range(result.shape[0]):
        state = result.at[i, 'state']
        state_count_dict[state] += result.at[i, 'count']

    result['percentage'] = 0.0
    for i in range(result.shape[0]):
        state = result.at[i, 'state']
        result.at[i, 'percentage'] = round(100 * result.at[i, 'count'] / float(state_count_dict[state]), 2)

    result.to_csv(path_or_buf=res, sep=',', header=True, index=False, index_label=None, \
                  columns=['id', 'state', 'disease', 'count', 'percentage', 'SI_index'])

def get_top_disease(res, n = 10):
    '''
    Get top n diseases based on the total ranks of diseases over all US states
    and write out results to a csv file
    '''
    result = pd.read_csv(res, sep=',', header=0)
    states = set(result['state'].values)
    states_excluded = set(['American Samoa', 'Guam', 'Northern Mariana Islands', \
                           'Puerto Rico', 'Virgin Islands'])
    disease = set(result['disease'].values)
    disease_count_dict = {item: 0 for item in disease}

    for state in states - states_excluded:
        res_state = result[result['state'] == state]
        for i, item in enumerate(res_state['disease'], start=1):
            disease_count_dict[item] += i
    res = Counter(disease_count_dict)

    top_diseases = [item[0] for item in res.most_common()[-n:]]
    top_diseases = list(reversed(top_diseases))
    res_top_diseases = result[result['disease'].isin(top_diseases)]
    res_top_diseases = res_top_diseases[res_top_diseases['state'].isin(states - states_excluded)]

    top_diseases_rank = {item: i for i, item in enumerate(top_diseases, start=1)}
    res_top_diseases['rank'] = 0
    res_top_diseases.reset_index(drop=True, inplace=True)
    for i in range(res_top_diseases.shape[0]):
        res_top_diseases.at[i, 'rank'] = top_diseases_rank[res_top_diseases.at[i, 'disease']]

    res_top_diseases.sort(columns=['state', 'rank'], axis=0, ascending=[True, True], inplace=True)
    res_top_diseases.to_csv(path_or_buf='results_top_{}.csv'.format(n), sep=',', header=True, index=False, \
                            columns=['id', 'state', 'disease', 'count', 'percentage', 'SI_index', 'rank'], \
                            index_label=None)
    return top_diseases

def get_top_disease_abs_count(results_top, n=10):
    '''
    Get the total counts of the top n diseases
    '''
    result = pd.read_csv(results_top, sep=',', header=0)
    disease = result['disease'][:n].values
    disease_count_dict = {item: 0 for item in disease}
    for d in disease:
        disease_count = result[result['disease'] == d]['count'].sum()
        disease_count_dict[d] = disease_count
    return disease_count_dict

if __name__=="__main__":
    pass


import os
import json
import re
import time
import pandas as pd
import numpy as np
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def find_State(loc, stateSearchDict, citySearchDict):
    '''
    Input state/city SearchDict: keys must be in lowercase
    Return state: state abbr in uppercase or None
    '''
    loc = loc.lower()
    temp = re.findall(r"[\w]+", loc)
    for item in temp:
        try:
            state = stateSearchDict[item]
            return state.upper()
        except:
            try:
                state = citySearchDict[item]
                return state.upper()
            except:
                pass

    temp = re.split(';|,|#|@|:|\.|\*|\~|\&|\^|\(|\)', loc)
    for item in temp:
        item = item.split()
        for i in range(2, len(item)+1):
            name = ' '.join(item[:i])
            try:
                state = stateSearchDict[name]
                return state.upper()
            except:
                try:
                    state = citySearchDict[name]
                    return state.upper()
                except:
                    pass
                
def find_Disease(text, keywordsList):
    '''
    Input keywordsList: keyword elements must be in lowercase
    '''
    text = text.lower()
    result = []
    for item in keywordsList:
        if item in text:
            result.append(item)
    return result

def load_Cities(cityFile):
    '''
    Return citySearchDict: city/state pairs in lowercase
    '''
    cityStateList = np.genfromtxt(cityFile, dtype='str', delimiter=',')
    citySearchDict = {item[1].lower(): item[0].lower() for item in cityStateList}
    cityList = cityStateList[:,1]
    cityDuplicate = [item for item, count in Counter(cityList).items() if count > 1]
    for city in cityDuplicate:
        temp = citySearchDict.pop(city.lower(), None)
    return citySearchDict

def load_States(stateFile):
    '''
    stateAbbrList: state abbreviation in uppercase
    stateSearchDict: abbr/fullname & abbr/abbr pairs in lowercase
    '''
    stateList = np.genfromtxt(stateFile, dtype='str', delimiter=',')
    stateAbbrList = stateList[:,0]
    stateFullNameList = stateList[:,1]
    stateSearchDict = {item[0].lower(): item[1].lower() for item in zip(stateFullNameList, stateAbbrList)}
    stateSearchDict2 = {item.lower(): item.lower() for item in stateAbbrList}
    stateSearchDict.update(stateSearchDict2)
    return stateAbbrList, stateSearchDict

def result_convert_sort(csv_filename, stateFile):
    '''
    Sort results by state (ASC) and count (DESC)
    Convert state names to full names to ensure consistency with us-states.json
    '''
    stateList = np.genfromtxt(stateFile, dtype='str', delimiter=',')
    stateAbbrList, stateFullNameList = stateList[:,0], stateList[:,1]
    abbrFullDict = {item[0].upper(): item[1].title() for item in zip(stateAbbrList, stateFullNameList)}

    result = pd.read_csv(csv_filename + '.csv', sep=',', header=None, \
                         names=['state', 'disease', 'count', 'SI_index'])
    for i in range(result.shape[0]):
        result.at[i, 'state'] = abbrFullDict[result.at[i, 'state']]
    result.sort(columns=['state', 'count'], axis=0, ascending=[True, False], inplace=True)
    result.to_csv(path_or_buf='{}_sorted.csv'.format(csv_filename), sep=',', header=True, index=False, \
                  columns=['state', 'disease', 'count', 'SI_index'], index_label=None)
    return None

if __name__ == '__main__':
    state_path_filename = '../locInfo/USstates.csv'
    city_path_filename = '../locInfo/UScities.csv'
    stateAbbrList, stateSearchDict = load_States(state_path_filename)
    citySearchDict = load_Cities(city_path_filename)

    SI_analyzer = SentimentIntensityAnalyzer()
    
    partList = ['part1', 'part2', 'part3', 'part4']

    for part in partList:
        print 'Analyzing {}...'.format(part)
        with open('../keywords/kwds_{}'.format(part), 'r') as f:
            keywordsList = [item.strip().lower() for item in f]

        state_disease_count = {state: {kwd: [0, 0] for kwd in keywordsList} for state in stateAbbrList}

        datafile_dir = '../output/{}'.format(part)
        outputFiles = [f for f in os.listdir(datafile_dir) \
                             if os.path.isfile(os.path.join(datafile_dir, f))]

        t1 = time.time()
        tweet_count, stateMatch, failsCount = 0, 0, 0
        for output in outputFiles:
            with open(datafile_dir + '/' + output, 'r') as f:
                for i, data in enumerate(f):
                    try:
                        datajson = json.loads(data)
                        tweet_count += 1
                        #print tweet_count
                    except:
                        continue
                    text = datajson["text"]
                    loc = datajson["user"]["location"]

                    state = find_State(loc, stateSearchDict, citySearchDict)
                    if state:
                        #print state, loc
                        stateMatch += 1
                        kwds = find_Disease(data, keywordsList)
                        if len(kwds) == 0:
                            failsCount += 1
                            continue

                        Sentiment_idx = SI_analyzer.polarity_scores(text)['compound']
                        for item in kwds:
                            state_disease_count[state][item][0] += 1
                            state_disease_count[state][item][1] += Sentiment_idx
        t2 = time.time()

        # Save results
        with open('results.csv', 'a') as res:
            for state in state_disease_count:
                state_res = state_disease_count[state]
                for kwd in state_res:
                    disease_count, SI_idx_total = state_res[kwd]
                    SI_idx = 0 if disease_count == 0 else 100 * float(SI_idx_total) / disease_count
                    res.write('{},{},{},{}\n'.format(state, kwd, disease_count, SI_idx))
        print 'Elapsed Time for {}: {}s'.format(part, t2 - t1)
        print 'Total:{}; State Match: {}; Fails: {}\n'.format(tweet_count, stateMatch, failsCount)
    result_convert_sort('results', state_path_filename)
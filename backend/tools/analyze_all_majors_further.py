import os
import json
from collections import Counter

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

# from fuzzywuzzy import fuzz, process
import textdistance

import nltk
from nltk.corpus import stopwords

import multiprocessing
import signal
import time

from parallel_task_handler import ParallelTaskHandler

if __name__ == '__main__':
    PARENT_DIR = os.path.dirname(__file__)
    EXTRACTED_JSON_PATH = f'{PARENT_DIR}/json-dump/extracted'
    os.makedirs(EXTRACTED_JSON_PATH, exist_ok=True)

    ALL_RAW_MAJORS_PATH = f'{EXTRACTED_JSON_PATH}/all-majors.json'
    ALL_CLEANED_MAJORS_PATH = f'{EXTRACTED_JSON_PATH}/all-majors-cleaned.json'

    with open(ALL_CLEANED_MAJORS_PATH, 'r') as fp:
        all_cleaned_majors = json.load(fp)

    subset = all_cleaned_majors[::]
    # subset = all_cleaned_majors[:20]
    print(len(subset))

    def similarity_scorer(seq):
        return textdistance.ratcliff_obershelp.normalized_similarity(*seq)


    def create_tasks(majors):
        task_params = []
        for first_major in majors:
            for second_major in majors:
                task_params += [(first_major, second_major)]
        return task_params

    similarity_calculator = ParallelTaskHandler(create_tasks, similarity_scorer)

    start = time.time()
    arr = similarity_calculator.process_items(subset)
    end = time.time()
    print(end - start)
    arr = np.asarray(arr).reshape((len(subset), len(subset)))

    df = pd.DataFrame(arr, columns=subset, index=subset)
    df.to_csv('test.csv', index=False)
    sns.heatmap(df, annot=True, fmt='.1f')
    plt.subplots_adjust(left=0.25, right=0.9, top=1.0, bottom=0.25)
    plt.show()

    all_words = (' '.join(all_cleaned_majors)).split()
    print(len(all_words))
    all_words = [word for word in all_words if len(word) > 1 and word.lower() not in stopwords.words("english")]
    print(len(all_words))
    counter = Counter(all_words)
    most_common = counter.most_common()
    print(len(most_common))

    # df2 = pd.DataFrame(most_common[::], columns=['word', 'count'])
    # print(df2['word'].value_counts()[:100])

    # df2['word'].value_counts()[:100].plot.barh(x='count', y='word')

    names, counts = np.asarray(most_common[::-1][1300:]).T.tolist()

    indexes = np.arange(len(names))
    width = 0.7
    plt.barh(indexes, counts, width)
    plt.yticks(indexes + width * 0.5, names)
    plt.xticks(counts)
    plt.show()

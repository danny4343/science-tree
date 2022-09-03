from os.path import exists
from datetime import datetime
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt

def log(string):
    to_write = f'{string} - {datetime.now()}\n'
    if exists('log.txt'):
        with open('log.txt', 'a', newline='', encoding='utf-8') as f:
            f.write(to_write)
    else:
        with open('log.txt', 'w', newline='', encoding='utf-8') as f:
            f.write(to_write)
            
def isInRef(domain):
    # dictionary for getting journal name from url
    journals_df = pd.read_csv('domain_to_journal.csv', delimiter='\t')
    journal_ref = pd.Series(journals_df.journal.values,index=journals_df.domain).to_dict()
    # dict: journal_ref['url'] = journal name
    
    if not(domain in journal_ref.keys()):
        if "doi" in domain:
            return False
        else:
            global unknown
            log(f'!!! {domain} !!!')
            return False
    else: return True
        
        
def plot_top_words(model, feature_names, n_topics, n_top_words, title):
    rows = ((n_topics-1) // 5) + 1
    fig, axes = plt.subplots(rows, 5, figsize=(30, (4*rows)), sharex=True) # 1x5 plot
    axes = axes.flatten()
    for topic_idx, topic in enumerate(model.components_): # topic_idx is number 0-#topics-1, topic is array of floats
        top_features_ind = topic.argsort()[: -n_top_words - 1 : -1] # finds indeces of n top words
        top_features = [feature_names[i] for i in top_features_ind] # gets the actual words
        weights = topic[top_features_ind] # gets weight
        ax = axes[topic_idx]

        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f"Topic {topic_idx}", fontdict={"fontsize": 20})
        ax.invert_yaxis()
        ax.tick_params(axis="both", which="major", labelsize=20)
        for i in "top right left".split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=20)

    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
    plt.show()
    

    
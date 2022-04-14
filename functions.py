from os.path import exists
from datetime import datetime
import pandas as pd

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
        
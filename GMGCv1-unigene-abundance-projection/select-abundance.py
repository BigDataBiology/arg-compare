import pandas as pd
from os import makedirs
g = pd.read_table('./GMGC10.AntibioticResistance.tsv', index_col=0)
interesting = set(g.index)

makedirs('unigene-summary', exist_ok=True)
with open('unigene-summary/GMGC10.sample-abundance-selected.tsv', 'wt') as out:
    is_first = True
    for ch in pd.read_table('./GMGC10.sample-abundance.tsv.xz', chunksize=100000, names=['unigene', 'sample', 'scaled', 'raw', 'raw_unique', 'normed10m'], skiprows=1):
        ch = ch[ch['unigene'].map(interesting.__contains__)]
        ch.to_csv(out, sep='\t', index=False, header=is_first)
        is_first = False

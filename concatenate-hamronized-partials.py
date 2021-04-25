import os
import pandas as pd
from glob import glob

deeparg = []
for f in sorted(glob('partials.deeparg/*')):
    if os.stat(f).st_size == 0:
        continue
    f = pd.read_table(f, index_col='input_sequence_id')
    deeparg.append(f)
deeparg = pd.concat(deeparg)
deeparg.to_csv('data/tables/deeparg.tsv', sep='\t')

for db in ['resfinder', 'card', 'argannot', 'ncbi', 'megares']:
    partials = []
    for f in sorted(glob(f'partials.abricate/*{db}*.hamronized')):
        if os.stat(f).st_size == 0: continue
        partials.append(pd.read_table(f, index_col='input_sequence_id'))
    pd.concat(partials).to_csv(f'data/tables/abricate.{db}.tsv', sep='\t')

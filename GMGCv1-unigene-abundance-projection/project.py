import pandas as pd
sel = pd.read_table('./GMGC10.sample-abundance-selected.tsv', index_col=0)

deeparg = pd.read_table('./GMGC10.AntibioticResistance.tsv', index_col=0, squeeze=True, usecols=[0,1])

#Only consider genes that have at least a single unique mapper
sel = sel.query('raw_unique > 0')

final_deeparg= sel.groupby('sample').apply(lambda df: df.groupby(deeparg).sum())
final_deeparg.to_csv('unigene-summary/deeparg.tsv', sep='\t', )

rgi = pd.read_table('./GMGC10.AntibioticResistance.tsv', index_col=0, squeeze=True, usecols=[0,2])
rgi = rgi.dropna()

final_rgi = sel.groupby('sample').apply(lambda df: df.groupby(rgi).sum())
final_rgi.to_csv('unigene-summary/rgi.tsv', sep='\t', )


for col in ['raw', 'raw_unique', 'normed10m']:
    f = final_deeparg[col]
    output = pd.pivot(f.reset_index(),
                index='sample',
                columns='deepARG',
                values='normed10m').fillna(0).astype(int)

    output.to_csv(f'unigene-summary/deeparg-{col}.tsv', sep='\t')

import pandas as pd

INPUTS = {
        'abricate_ARG_ANNOT': 'abricate.argannot.tsv.xz',
        'abricate_CARD': 'abricate.card.tsv.xz',
        'abricate_MEGARES': 'abricate.megares.tsv.xz',
        'abricate_NCBI': 'abricate.ncbi.tsv.xz',
        'abricate_RESFINDER': 'abricate.resfinder.tsv.xz',
        'abricate_RESFINDER_FG2': 'all_hamronized_abricate_resfinderfg.txt',
        }

deeparg = pd.read_table('computed/deeparg.tsv.xz', index_col=0, )
rgi = pd.read_table('computed/GMGC10.95nr.card.tsv.xz', index_col=0)



strict = rgi.query('Cut_Off == "Strict"')
rgi = rgi['Best_Hit_ARO']
rgi_strict = strict['Best_Hit_ARO']
deeparg = deeparg['gene_symbol'].squeeze().copy()

data = {'deepARG': deeparg,
        'rgi': rgi,
        'rgi_strict': rgi_strict,
        }

for k,fn in INPUTS.items():
    f = pd.read_table(f'computed/{fn}')
    s = f[['gene_symbol', 'input_sequence_id']]
    data[k] = s.groupby('input_sequence_id').apply(lambda df : ';'.join(df['gene_symbol'].values))

for k,s in data.items():
    print(k, len(s.index), len(set(s.index)), s.shape)
full = pd.DataFrame(data)

full.to_csv('GMGC10.AntibioticResistance.tsv', sep='\t')

import subprocess
from jug import TaskGenerator
from jug.utils import identity


@TaskGenerator
def run_sample(s):
    from os import path, makedirs
    import tempfile
    odir = path.join('outputs', 'resfinder', s)
    try:
        makedirs(odir)
    except:
        pass
    with tempfile.TemporaryDirectory() as tdir:
        subprocess.check_call([
            'ngless',
            '--trace',
            '--threads', '1',
            '--no-create-report',
            'preprocess-resfinder.ngl',
            s,
            tdir])


        if path.exists(path.join(tdir, 'preproc.pair.1.fq')):
            subprocess.check_call([
                'python',
                '../resfinder/run_resfinder.py',
                '--acquired',
                '--inputfastq',
                    path.join(tdir, 'preproc.pair.1.fq'),
                    path.join(tdir, 'preproc.pair.2.fq'),
                '-o', odir
                ])
        else:
            subprocess.check_call([
                'python',
                '../resfinder/run_resfinder.py',
                '--acquired',
                '--inputfastq',
                    path.join(tdir, 'preproc.fq'),
                '-o', odir
                ])
    return odir

@TaskGenerator
def concatenate_outputs(outputs):
    import pandas as pd
    from os import path
    oname = 'outputs/ResFinder_results_tab.GMGCv1.tsv'
    data = []
    for s,odir in outputs.items():
        tab = odir + '/ResFinder_results_tab.txt'
        if not path.exists(tab):
            continue
        ch = pd.read_table(tab)
        ch.insert(0, 'sample', s)
        data.append(ch)
    data = pd.concat(data)
    data.to_csv(oname, sep='\t', index=False)
    return oname

samples = [line.strip() for line in open('data/samples.txt')]
samples.sort()

outputs = {}
for s in samples:
    outputs[s] = run_sample(s)

outs = identity(outputs)
concatenate_outputs(outs)

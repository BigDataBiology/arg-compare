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
            'preprocess-resfinder.ngl',
            s,
            tdir])
        subprocess.check_call([
            'python',
            '../resfinder/run_resfinder.py',
            '--acquired',
            '--inputfastq',
                path.join(tdir, 'preproc.pair.1.fq.gz'),
                path.join(tdir, 'preproc.pair.2.fq.gz'),
            '-o', odir
            ])
    return odir

samples = [line.strip() for line in open('data/samples.txt')]
samples.sort()

outputs = {}
for s in samples:
    outputs[s] = run_sample(s)

outs = identity(outputs)
#build_table(outs)

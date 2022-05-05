import subprocess
from jug import TaskGenerator
from jug.utils import identity

@TaskGenerator
def run_sample(s):
    from os import path, makedirs, stat
    odir = 'outputs/deeparg.local-assembly/'+s
    orf_fname = 'orfs/'+s+'-assembled.mgm.fna'
    try:
        makedirs(odir)
    except:
        pass
    if stat(orf_fname).st_size == 0:
        return odir
    subprocess.check_call([
        'deeparg',
        'predict',
        '--model', 'LS',
        '--input', orf_fname,
        '--output', odir + '/output',
        '--data-path', 'deeparg_datadir'])
    return odir

samples = [line.strip() for line in open('data/samples.txt')]
samples.sort()

for s in samples:
    run_sample(s)


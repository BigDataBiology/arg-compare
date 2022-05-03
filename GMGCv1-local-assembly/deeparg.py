import subprocess
from jug import TaskGenerator
from jug.utils import identity

@TaskGenerator
def run_sample(s):
    from os import path, makedirs
    odir = 'outputs/deeparg.local-assembly/'+s
    try:
        makedirs(odir)
    except:
        pass
    subprocess.check_call([
        'deeparg',
        'predict',
        '--model', 'LS',
        '--input', 'orfs/'+s+'-assembled.mgm.fna',
        '--output', odir + '/output',
        '--data-path', 'deeparg_datadir'])
    return odir

samples = [line.strip() for line in open('data/samples.txt')]
samples.sort()

for s in samples:
    run_sample(s)


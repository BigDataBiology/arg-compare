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

@TaskGenerator
def cleanup_xz(basedir):
    import os
    import subprocess
    from glob import glob
    if os.path.exists(basedir  + '/output.align.daa'):
        os.unlink(basedir  + '/output.align.daa')
    if os.path.exists(basedir + '/output.align.daa.tsv'):
        subprocess.check_call(['xz', basedir + '/output.align.daa.tsv'])
    return basedir

@TaskGenerator
def concatenate_outputs(outputs, fname):
    import subprocess
    from os import path
    oname = 'outputs/'+fname + '.GMGCv1'
    is_first = True
    with open(oname, 'wt') as out:
        for basedir in outputs:
            ifile = basedir + '/' + fname
            if path.exists(ifile):
                with open(ifile) as ifile:
                    if not is_first:
                        ifile.readline() # skip first line
                    out.write(ifile.read())
                    is_first = False
    subprocess.check_call(['xz', oname])
    return oname + '.xz'


samples = [line.strip() for line in open('data/samples.txt')]
samples.sort()

outputs = []
for s in samples:
    outputs.append(cleanup_xz(run_sample(s)))

outputs = identity(outputs)

for fname in ['output.mapping.ARG', 'output.mapping.potential.ARG']:
    concatenate_outputs(outputs, fname)

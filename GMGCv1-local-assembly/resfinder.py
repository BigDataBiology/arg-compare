import subprocess
from jug import TaskGenerator
from jug.utils import identity

@TaskGenerator
def run_sample(s):
    from os import path, makedirs, stat
    import tempfile
    odir = 'outputs/resfinder.local-assembly/'+s
    ifname = 'assembled/'+s+'-assembled.fna'
    try:
        makedirs(odir)
    except:
        pass
    if stat(ifname).st_size == 0:
        return odir
    with tempfile.TemporaryDirectory() as tdir:
        fafile = tdir + '/copy.fna'
        with open(fafile, 'wb') as ofile:
            with open(ifname, 'rb') as ifile:
                while ch := ifile.read(1024*1024*8):
                    ofile.write(ch)
        subprocess.check_call([
            'python',
            '../resfinder/run_resfinder.py',
            '--acquired',
            '--inputfasta', fafile,
            '-o', odir])
    return odir


@TaskGenerator
def compress_tmp(odir):
    from glob import glob
    import subprocess
    for x in glob(f'{odir}/resfinder_blast/tmp/*xml'):
        subprocess.check_call([
            'xz',
            '--threads=8',
            x])
    return odir
@TaskGenerator
def compress_file(f):
    from glob import glob
    import subprocess
    subprocess.check_call([
        'xz',
        '--threads=8',
        f])
    return f + '.xz'
samples = [line.strip() for line in open('data/samples.txt')]
samples.sort()

outputs = []
for s in samples:
    outputs.append(compress_tmp(run_sample(s)))

outputs = identity(outputs)

@TaskGenerator
def concatenate_outputs(outputs):
    import pandas as pd
    from os import path
    oname = 'outputs/ResFinder_results_tab.GMGCv1.tsv'
    data = []
    for odir in outputs:
        s = path.split(odir)[-1]
        tab = odir + '/ResFinder_results_tab.txt'
        if not path.exists(tab):
            continue
        ch = pd.read_table(tab)
        ch.insert(0, 'sample', s)
        data.append(ch)
    data = pd.concat(data)
    data.to_csv(oname, sep='\t', index=False)
    return oname

compress_file(concatenate_outputs(outputs))

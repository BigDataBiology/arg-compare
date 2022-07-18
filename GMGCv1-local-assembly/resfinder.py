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
samples = [line.strip() for line in open('data/samples.txt')]
samples.sort()

outputs = []
for s in samples:
    compress_tmp(run_sample(s))
    #outputs.append(cleanup_xz(run_sample(s)))

#outputs = identity(outputs)

#for fname in ['output.mapping.ARG', 'output.mapping.potential.ARG']:
#    concatenate_outputs(outputs, fname)

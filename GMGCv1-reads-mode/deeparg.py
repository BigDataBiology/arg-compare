import subprocess
from jug import TaskGenerator

DATA_DIR = '/scratch/coelho/deeparg_datadir/'

@TaskGenerator
def deeparg_get_data(data_dir):
    subprocess.check_call([
        'deeparg',
        'download_data',
        '-o', data_dir])
    return data_dir

def run_deeparg(data_dir, fq_1, fq_2, out):
    subprocess.check_call([
        'deeparg',
        'short_reads_pipeline',
        '--forward_pe_file', fq_1,
        '--reverse_pe_file', fq_2,
        '--output_file', out,
        '-d', data_dir])

@TaskGenerator
def run_sample(data_dir, s):
    from os import path, makedirs
    odir = path.join('outputs', 'deeparg', s)
    try:
        makedirs(odir)
    except:
        pass
    subprocess.check_call([
        'ngless',
        '--trace',
        '--threads', '8',
        'preprocess.ngl', s])
    run_deeparg(data_dir,
                path.join(odir, 'preproc.pair.1.fq.gz'),
                path.join(odir, 'preproc.pair.2.fq.gz'),
                path.join(odir, 'output.deeparg'))
    return odir


samples = [line.strip() for line in open('data/samples.txt')]
samples.sort()

data_dir = deeparg_get_data(DATA_DIR)

for s in samples:
   run_sample(data_dir, s)


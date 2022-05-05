import subprocess
from jug import TaskGenerator
from jug.utils import identity

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

@TaskGenerator
def clean_up_deeparg_outputs(basedir):
    from glob import glob
    import os
    for f in glob(basedir + '/preproc.*') + glob(basedir + '/*.bam') + [basedir + '/output.deeparg.clean', basedir + '/output.deeparg.clean.sam']:
        if os.path.exists(f):
            os.unlink(f)

    return basedir

@TaskGenerator
def xz_files(basedir):
    print(basedir)
    from glob import glob
    import subprocess
    for f in glob(basedir + '/*'):
        if not f.endswith('.xz'):
            subprocess.check_call(['xz', f])
    return basedir


@TaskGenerator
def build_table(outputs):
    import pandas as pd
    data = {}
    for s, basedir in outputs.items():
        data[s] = pd.read_table(
                    basedir + '/output.deeparg.clean.deeparg.mapping.ARG.merged.quant.xz',
                    names=['Symbol', 'category', 'nrReads', 'B', 'C', 'D']) \
                            .set_index("Symbol")['nrReads']
    data = pd.DataFrame(data).fillna(0).astype(int)
    data.to_csv('outputs/deepARG-read-mode.tsv', sep='\t')
    return 'outputs/deepARG-read-mode.tsv'


samples = [line.strip() for line in open('data/samples.txt')]
samples.sort()

data_dir = deeparg_get_data(DATA_DIR)

deeparg_outputs = {}
for s in samples:
    deeparg_outputs[s] = xz_files(clean_up_deeparg_outputs(run_sample(data_dir, s)))

outs = identity(deeparg_outputs)
build_table(outs)

from jug import TaskGenerator, bvalue
from jug.utils import jug_execute
import itertools
import subprocess

MAX_SEQ_CHUNKS = 1000

@TaskGenerator
def split_seq_file(fa):
    from os import makedirs, path
    from fasta import fasta_iter
    import gzip
    makedirs('partials', exist_ok=True)
    basename = path.basename(fa)
    cur_n = MAX_SEQ_CHUNKS + 1
    ix = 0
    out = None
    partials = []
    for h, seq in fasta_iter(fa):
        if cur_n >= MAX_SEQ_CHUNKS:
            if fa.endswith('.faa.gz'):
                partials.append(f'partials/{basename}_block_{ix:04}.faa.gz')
            elif fa.endswith('.fna.gz'):
                partials.append(f'partials/{basename}_block_{ix:04}.fna.gz')
            else:
                raise ValueError(f'Unexpected file name: {fa}')
            out = gzip.open(partials[-1], compresslevel = 1, mode = 'wt')
            cur_n = 0
            ix += 1
        out.write(f'>{h}\n{seq}\n')
        cur_n +=1
    out.close()
    return partials

@TaskGenerator
def run_rgi(faa):
    import subprocess
    import tempfile
    from os import makedirs
    import shutil
    makedirs('partials.rgi', exist_ok=True)
    oname = faa.replace('partials', 'partials.rgi').replace('faa.gz', 'rgi.tsv')
    with tempfile.TemporaryDirectory() as tdir:
        if faa.endswith('.gz'):
            import gzip
            faa_expanded = tdir + '/data.faa.gz'
            with gzip.open(faa, 'rb') as ifile, \
                open(faa_expanded, 'wb') as ofile:
                while True:
                    block = ifile.read(8192)
                    if not block:
                        break
                    ofile.write(block)
            faa = faa_expanded
        tmp_oname = tdir + '/RGI_output'
        subprocess.check_call([
            'rgi', 'main',
            '-t', 'protein',
            '-i', faa,
            '-o', tmp_oname])
        shutil.copy(tmp_oname + '.txt', oname)
    return oname

@TaskGenerator
def run_abricate(fna, db):
    import subprocess
    from os import makedirs
    makedirs('partials.abricate', exist_ok=True)
    oname = fna.replace('partials', 'partials.abricate').replace('fna.gz', f'abricate.{db}.tsv')
    with open(oname, 'wb') as out:
        subprocess.check_call([
            'abricate',
            '--db', db,
            fna],
            stdout=out)
    return oname


@TaskGenerator
def run_deeparg(fna):
    import subprocess
    from os import makedirs
    makedirs('partials.deeparg', exist_ok=True)
    oname = fna.replace('partials', 'partials.deeparg').replace('fna.gz', 'deeparg.tsv')

    subprocess.check_call([
        'conda', 'run', '-n', 'deeparg_env',
        'deeparg', 'predict',
        '--model', 'LS',
        '-i', fna,
        '-o', oname,
        '-d', './deeparg_data',
        '--type', 'nucl',
        '--min-prob', '0.8',
        '--arg-alignment-identity', '30',
        '--arg-alignment-evalue', '1e-10',
        '--arg-num-alignments-per-entry', '1000'])
    return oname


@TaskGenerator
def concat_partials(partials, oname):
    import pandas as pd
    partials = [pd.read_table(p, index_col =0, comment = '#') for p in partials]
    full = pd.concat(partials)
    full.to_csv(oname, sep='\t')
    return oname




@TaskGenerator
def run_rgi_hamronize(run_rgi_input, rgi_output):
    import subprocess
    rgi_software_version = subprocess.check_output(
            ['conda', 'run', '-n', 'arg-compare',
                'rgi', 'main', '--version']).decode('utf-8').strip()
    rgi_db_version = subprocess.check_output(
            ['conda', 'run', '-n', 'arg-compare',
                'rgi', 'database', '--version']).decode('utf-8').strip()

    oname = rgi_output+'.hamronized'
    with open(oname, 'wb') as out:
        subprocess.check_call([
            'conda', 'run', '-n', 'hamronization',
            'hamronize', 'rgi',
            '--input_file_name', run_rgi_input,
            '--analysis_software_version', rgi_software_version,
            '--reference_database_version', rgi_db_version,
            rgi_output],
            stdout=out)
    return oname



@TaskGenerator
def run_abricate_hamronize(abricate_output):
    import subprocess
    abricate_software_version = subprocess.check_output(
        ['conda', 'run', '-n', 'arg-compare',
            'abricate', '--version']).decode('utf-8').strip()
    for line in subprocess.check_output(
        ['conda', 'run', '-n', 'arg-compare',
            'abricate', '--list']).decode('utf-8').split('\n'):
                tokens = line.split('\t')
                if tokens[0] == 'ncbi':
                    abricate_db_version = tokens[-1]

    oname = abricate_output+'.hamronized'
    with open(oname, 'wb') as out:
        subprocess.check_call([
            'conda', 'run', '-n', 'hamronization',
            'hamronize', 'abricate',
            abricate_output,
            '--analysis_software_version', abricate_software_version,
            '--reference_database_version', abricate_db_version],
            stdout=out)
    return oname

@TaskGenerator
def run_deeparg_hamronize(deeparg_input, deeparg_output):
    import subprocess
    deeparg_software_version = 'v2'
    deeparg_db_version = 'v2'
    oname = deeparg_output+'.hamronized'
    with open(oname, 'wb') as out:
        subprocess.check_call([
            'conda', 'run', '-n', 'hamronization',
            'hamronize', 'deeparg',
            '--input_file_name', deeparg_input,
            '--analysis_software_version', deeparg_software_version,
            '--reference_database_version', deeparg_db_version,
            deeparg_output + '.mapping.ARG'],
            stdout=out)
    return oname


splits_faa = split_seq_file('data/GMGC10.wastewater.95nr.test_10k.faa.gz')
partials = []
for faa in (bvalue(splits_faa)):
    partials.append(
            run_rgi_hamronize(faa, run_rgi(faa)))
concat_partials(partials, 'outputs/rgi.full.tsv.gz')

splits_fna = split_seq_file('data/GMGC10.wastewater.95nr.test_10k.fna.gz')
for fa in bvalue(splits_fna):
    for db in ['resfinder', 'card','argannot','ncbi','megares']:
        run_abricate_hamronize(run_abricate(fa, db))


    run_deeparg_hamronize(fa, run_deeparg(fa))

@TaskGenerator
def run_hamronize_summarize(reports, combined):
    '''Combine outputs of all the tools

    Parameters
    ----------
    reports : list of str
       List of file paths, each being the result of a hamronize operation

    combined : str
        Output path for combined report

    Returns
    -------
    combined : str
        Returns the combined path (for convenience)
    '''
    subprocess.check_call([
        'conda', 'run', '-n', 'hamronization',
        'hamronize', 'summarize',
        '-o', combined,
        '-t', 'tsv',
        ] + reports)
    return combined

run_hamronize_summarize(reports, 'summary.tsv')


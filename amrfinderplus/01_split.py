def split_seq_file(infile,outdir):
    from os import path
    from fasta import fasta_iter

    basename = path.basename(infile)
    MAX_SEQ_CHUNKS = 600000
    cur_n = MAX_SEQ_CHUNKS + 1
    ix = 0
    for h, seq in fasta_iter(infile):
        if cur_n >= MAX_SEQ_CHUNKS:
            outfile = f'{outdir}/{basename}_block_{ix:03}.faa'
            out = open(outfile,"wt")
            cur_n = 0
            ix += 1
        out.write(f'>{h}\n{seq}\n')
        cur_n +=1
    out.close()

INPUT_FILE = "~/data/GMGC1/GMGC10.95nr.faa.gz"
OUTPUT_DIR = "~/data/split"
split_seq_file(INPUT_FILE,OUTPUT_DIR)
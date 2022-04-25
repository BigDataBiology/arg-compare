# Results and codes for ARGs-OAP

## ARGs-OAP contig mode:

Sargfam is downloaded from https://github.com/xiaole99/Sargfam

Use hmmscan to map `GMGC10.wastewater.95nr.faa` against Sargfam.

But I suggest to use hmmsearch to map Sargfam against `GMGC10.wastewater.95nr.faa`.

hmmsearch is faster and does the same things as hmmscan(the results are very similar).

Result is `args_oap_hmm_result.tsv` .

## ARGs-OAP read mode:

### Installation:
ARGs-OAP is downloaded as https://github.com/biofuture/Ublastx_stageone  :

1. Download argoapv2.5.sif: "Download the singularity verion of the pipeline image from the following link (https://ndownloader.figshare.com/files/25953791), due to large file size limitation of github, the sif image is deposited on figshare"

2. Download singularity: "Recommended version 3.5.3 singularity[https://sylabs.io/guides/3.0/user-guide/installation.html] is used"

*Note:* This official singularity installation is unable for HW server & ISTBI server for some reason.We found a conda version of singularity https://anaconda.org/conda-forge/singularity

### Run ARGs-OAP
1. Prepare the meta-data file of your samples:
   It's clear in https://github.com/biofuture/Ublastx_stageone

*Note:* The `Name` must be consistant with sample name.

2. Run ARGs-OAP

(1) Input:

All reads are stored in `inputdir`. All sample metadata are in `metadata.txt`

*Note:* 

a. The input name of ARGs-OAP must be end with .fq/.fq.gz.If our downloaded reads files are end with .fastq.gz,we need to change all the name manually.

b. If reads is compressed files, it's better to store it in the backup folder, because ARGs OAP will unzip them in place without retaining the original compressed files.

c. It can't process single-end reads, so only process paired-end reads samples.

(2) Output:

All results will be generated in `outdir`.

(3) Command:

```
singularity exec -B /home/yiqian/AMR/ARG-OAP/inputdir /home/yiqian/AMR/ARG-OAP/argoapv2.5.sif /home/argsoapv2.5/argoap_version2.5 -i /home/yiqian/AMR/ARG-OAP/inputdir -m /home/yiqian/AMR/ARG-OAP/metadata.txt -o /home/yiqian/AMR/ARG-OAP/test_out -n 8 -z
```

*Note:* It's better to use absolute path to avoid additional error. `-z` is "whether the fq files were .gz format, if -z, then firstly gzip -d, default(none)"


## Hamronization:

hAMRonization can't support ARGs-OAP, so I hamronized these results using my own scripts.

For contig mode result `args_oap_hmm_result.tsv`:

Script is `ARGsOAP_hmm_hamronized.py`, hamronized result is `ARGsOAP_hmm_hamronized.tsv`

For read mode result `args_oap_reads_result.tsv`:

Script is `ARGsOAP_reads_hamronized.py`, hamronized result is `ARGsOAP_reads_hamronized.tsv`

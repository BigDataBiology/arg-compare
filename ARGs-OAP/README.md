# Results and codes for ARGs-OAP

## ARGs-OAP contig mode:

Sargfam is downloaded from https://github.com/xiaole99/Sargfam

Use hmmscan to map `GMGC10.wastewater.95nr.faa` against Sargfam.

But I suggest to use hmmsearch to map Sargfam against `GMGC10.wastewater.95nr.faa`.

hmmsearch is faster and does the same things as hmmscan(the results are very similar).

Result is `args_oap_hmm_result.tsv` .

## ARGs-OAP read mode:

ARGs-OAP is downloaded as https://github.com/biofuture/Ublastx_stageone

It can't process single-end reads, so only process paired-end reads of wastewater samples.

All samples are in `metadata.txt`

Result are `args_oap_reads_result.tsv` and `stage2output.normalize_cellnumber.gene.txt`.

## Hamronization:

hAMRonization can't support ARGs-OAP, so I hamronized these results using my own scripts.

For contig mode result `args_oap_hmm_result.tsv`:

Script is `ARGsOAP_hmm_hamronized.py`, hamronized result is `ARGsOAP_hmm_hamronized.tsv`

For read mode result `args_oap_reads_result.tsv`:

Script is `ARGsOAP_reads_hamronized.py`, hamronized result is `ARGsOAP_reads_hamronized.tsv`
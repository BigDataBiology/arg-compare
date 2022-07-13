# Results and codes for AMRFinderPlus
## Split GMGC unigenes because of memory limitation
`01_split.py`

## AMRFinderPlus Installation
Install AMRFinderPlus as https://github.com/ncbi/amr/wiki/Installing-AMRFinder
```
conda activate amrfinderplus -c conda-forge -c bioconda ncbi-amrfinderplus
amrfinder -u
conda activate amrfinderplus
```

## Run AMRFinderPlus protein mode:
Run on the whole GMGC unigenes
`02_run_amrfinderplus.sh`

Example
```
curl -O https://raw.githubusercontent.com/ncbi/amr/master/test_prot.fa
amrfinder -p /home1/duanyq/AMR/amrfinder/test_prot.fa --threads 64 -o /home1/duanyq/AMR/amrfinder/test
```

## Run AMRFinderPlus contig mode:
Example
```
amrfinder -n /work/yiqian/resfinder/data/SAMN03922462-assembled.fa --threads 64 -o /work/yiqian/amrfinderplus/output/orf

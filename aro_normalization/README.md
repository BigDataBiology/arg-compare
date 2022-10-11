**ARO ontology to facilitate comparison of outputs with different gene_names**

**Description:**
- Annotate ARGs on [GMGC](https://gmgc.embl.de/download.cgi) using [RGI](https://github.com/arpcard/rgi#running-rgi-main-with-protein-sequences),[DeepARG](https://bench.cs.vt.edu/deeparg),[ARGs-OAP](https://smile.hku.hk/SARGs),[ABRicate](https://github.com/tseemann/abricate),[ResFinder](https://bitbucket.org/genomicepidemiology/resfinder/src/master/) and [AMRFinderPlus](https://github.com/ncbi/amr).
- Normalize different outputs by [hAMRonization](https://github.com/pha4ge/hAMRonization).
- Annotate ARO number by [argNorm](https://github.com/BigDataBiology/argNorm).

**Some special instructions：**
The results are generated from different tools,different input modes of tools and different database.
- Different tools contain:
[RGI](https://github.com/arpcard/rgi#running-rgi-main-with-protein-sequences),[DeepARG](https://bench.cs.vt.edu/deeparg),[ARGs-OAP](https://smile.hku.hk/SARGs),[ABRicate](https://github.com/tseemann/abricate),[ResFinder](https://bitbucket.org/genomicepidemiology/resfinder/src/master/) and [AMRFinderPlus](https://github.com/ncbi/amr)
- Different modes:
  Some tools can support different input file.However,different input mode can probably generate different results. 
  - Protein mode: input file is protein .faa file.
  - Assembly mode: input file is contig .fna file.
  - Read mode: input file is read .fq file.
- Different database:
  Some tools have their own specific databases,such as ARGs-OAP has SARGdb.
  Some tools can annotate from different databases,such as ABRicate can annotate from CARD,ResFinder,ARG-ANNOT,MEGARes and NCBI database.

# File Summary
- RGI.card.hamronized.tsv.xz: RGI/protein mode/CARD
- deeparg.protein.hmr.aro.tsv.xz: Deeparg/protein mode
- deeparg.assembly.aro.tsv.xz: Deeparg/assembly mode
- deepARG-read-mode.tsv.xz: Deeparg/read mode
- argsoap.protein.hmr.aro.tsv.xz: ARGs-OAP/protein mode/SARGdb
- abricate.card.tsv.xz: Abricate/protein mode/CARD
- abricate.resfinder.hmr.aro.tsv: Abricate/protein mode/Resfinder
- abricate.argannot.hmr.aro.tsv: Abricate/protein mode/ARG-ANNOT
- abricate.ncbi.hmr.aro.tsv: Abricate/protein mode/NCBI
- abricate.megares.hmr.aro.tsv: Abricate/protein mode/MEGARes
- resfinder.assembly.aro.tsv: Resfinder/assembly mode/Resfinder
- amrfinderplus.protein.aro.tsv: AMRFinderPlus/protein mode/NCBI

# DETAIL
## RGI
[The Resistance Gene Identifier (RGI)](https://github.com/arpcard/rgi#running-rgi-main-with-protein-sequences) is used to predict antibiotic resistome(s) from protein or nucleotide data based on homology and SNP models. The application uses reference data from the Comprehensive Antibiotic Resistance Database (CARD).

### Protein mode
#### Result file
- [RGI.card.hamronized.tsv.xz](https://github.com/BigDataBiology/arg-compare/blob/master/computed/RGI.card.hamronized.tsv.xz)
- Column specification
*'reference_accession'* column is the ARO number from CARD.
*'input_sequence_id'* column is the GMGC unigene accession.
#### Run RGI command
```
rgi main -t protein -i faa -o tmp_oname
```
#### Hamronize command
```
hamronize rgi --input_file_name run_rgi_input --analysis_software_version rgi_software_version --reference_database_version rgi_db_version rgi_output
```
> Note that CARD RGI already uses ARO, thus there is no need to use argNorm.



## DeepARG
[DeepARG](https://bench.cs.vt.edu/deeparg) is a machine learning solution that uses deep learning to characterize and annotate antibiotic resistance genes in metagenomes. It is composed of two models for two types of input: short sequence reads and gene-like sequences.

### Protein mode
#### Result file
- [deeparg.protein.hmr.aro.tsv.xz](https://github.com/BigDataBiology/arg-compare/blob/676af9a0886234608b6c6ecd0c35da53d777ed3e/aro_normalization/deeparg.protein.hmr.aro.tsv.xz)
- Column specification
*'input_sequence_id'* column is the GMGC unigene accession.
#### Run DeepARG command
```
deeparg predict --model LS -i fna -o oname -d ./deeparg_data --type nucl --min-prob 0.8 --arg-alignment-identity 30 --arg-alignment-evalue 1e-10 --arg-num-alignments-per-entry 1000
```
#### Hamronize command
```
hamronize deeparg --input_file_name deeparg_input --analysis_software_version deeparg_software_version --reference_database_version deeparg_db_version deeparg_output + '.mapping.ARG'
```

### Assembly mode
#### Result file
- [deeparg.assembly.aro.tsv.xz](https://github.com/BigDataBiology/arg-compare/blob/676af9a0886234608b6c6ecd0c35da53d777ed3e/aro_normalization/deeparg.assembly.aro.tsv.xz)
- Column specification
*'read_id'* column is the accession of **reads**(???or contigs?) in GMGC sample.


#### Run DeepARG command
```
deeparg predict --model LS --input orf_fname --output odir + '/output' --data-path deeparg_datadir
```
>Note that hamronization is optional when annotate ARO using argNorm.

### Read mode
#### Result file
- [deepARG-read-mode.tsv.xz](https://github.com/BigDataBiology/arg-compare/blob/master/GMGCv1-reads-mode/computed/deepARG-read-mode.tsv.xz)
- Column specification
column name is the accession of GMGC samples.
#### Run DeepARG command
```
deeparg short_reads_pipeline --forward_pe_file fq_1 --reverse_pe_file fq_2 --output_file out -d data_dir
```
>Note that read mode output is the ARG abundance across samples.



## ARGs-OAP
[ARGs-OAP](https://smile.hku.hk/SARGs) is an online analysis pipeline for anti-biotic resistance genes detection from meta-genomic data using an integrated structured ARG-database.

### Protein mode
#### Result file
- [argsoap.protein.hmr.aro.tsv.xz](https://github.com/BigDataBiology/arg-compare/blob/676af9a0886234608b6c6ecd0c35da53d777ed3e/aro_normalization/argsoap.protein.hmr.aro.tsv.xz)
- Column specification
*'input_sequence_id'* column is the GMGC unigene accession.
#### Run ARGs-OAP command(directly searching SARGFam database)
```
hmmscan --cut_ga --tblout args_oap_hmm_result.tsv Sargfam.hmm GMGC10.wastewater.95nr.faa.gz
```
>Note that hAMRonization doesn't support ARGs-OAP,thus we do hAMRonization manually.



## ABRicate
[ABRicate](https://github.com/tseemann/abricate) is Mass screening of contigs for antimicrobial resistance or virulence genes. It comes bundled with multiple databases: NCBI, CARD, ARG-ANNOT, Resfinder, MEGARES, EcOH, PlasmidFinder, Ecoli_VF and VFDB.

### Protein mode
#### CARD database
##### Result file
- [abricate.card.tsv.xz](https://github.com/BigDataBiology/arg-compare/blob/master/computed/abricate.card.tsv.xz)
- Column specification
*'input_sequence_id'* column is the GMGC unigene accession.
##### Run ABRicate command
```
abricate --db card fna
```
##### Hamronize command
```
hamronize abricate abricate_output --analysis_software_version abricate_software_version --reference_database_version abricate_db_version
```

#### ResFinder database
##### Result file
- [abricate.resfinder.hmr.aro.tsv](https://github.com/BigDataBiology/arg-compare/blob/676af9a0886234608b6c6ecd0c35da53d777ed3e/aro_normalization/abricate.resfinder.hmr.aro.tsv)
- Column specification
*'input_sequence_id'* column is the GMGC unigene accession.
##### Run ABRicate command
```
abricate --db resfinder fna
```
##### Hamronize command
```
hamronize abricate abricate_output --analysis_software_version abricate_software_version --reference_database_version abricate_db_version
```

#### ARG-ANNOT database
##### Result file
- [abricate.argannot.hmr.aro.tsv](https://github.com/BigDataBiology/arg-compare/blob/676af9a0886234608b6c6ecd0c35da53d777ed3e/aro_normalization/abricate.argannot.hmr.aro.tsv)
- Column specification
*'input_sequence_id'* column is the GMGC unigene accession.
##### Run ABRicate command
```
abricate --db argannot fna
```
##### Hamronize command
```
hamronize abricate abricate_output --analysis_software_version abricate_software_version --reference_database_version abricate_db_version
```

#### NCBI database
##### Result file
- [abricate.ncbi.hmr.aro.tsv](https://github.com/BigDataBiology/arg-compare/blob/676af9a0886234608b6c6ecd0c35da53d777ed3e/aro_normalization/abricate.ncbi.hmr.aro.tsv)
- Column specification
*'input_sequence_id'* column is the GMGC unigene accession.
##### Run ABRicate command
```
abricate --db ncbi fna
```
##### Hamronize command
```
hamronize abricate abricate_output --analysis_software_version abricate_software_version --reference_database_version abricate_db_version
```

#### MEGARes database
##### Result file
- [abricate.megares.hmr.aro.tsv](https://github.com/BigDataBiology/arg-compare/blob/676af9a0886234608b6c6ecd0c35da53d777ed3e/aro_normalization/abricate.megares.hmr.aro.tsv)
- Column specification
*'input_sequence_id'* column is the GMGC unigene accession.
##### Run ABRicate command
```
abricate --db megares fna
```
##### Hamronize command
```
hamronize abricate abricate_output --analysis_software_version abricate_software_version --reference_database_version abricate_db_version
```



## ResFinder
[ResFinder](https://bitbucket.org/genomicepidemiology/resfinder/src/master/) identifies acquired antimicrobial resistance genes in total or partial sequenced isolates of bacteria.

### Assembly mode
#### Result file
- [resfinder.assembly.aro.tsv](https://github.com/BigDataBiology/arg-compare/blob/676af9a0886234608b6c6ecd0c35da53d777ed3e/aro_normalization/resfinder.assembly.aro.tsv)
- Column specification
*'sample'* column is the GMGC sample accession.
#### Run ResFinder command
```
python ../resfinder/run_resfinder.py --acquired --inputfasta fafile -o odir
```



## AMRFinderPlus
[AMRFinderPlus](https://github.com/ncbi/amr) and the accompanying database are designed to find acquired antimicrobial resistance genes and some point mutations in protein or assembled nucleotide sequences. We have also added "plus" stress, head, and biocide resistance as well as some virulence factors and E. coli antigens.
### Protein mode
#### Result file
- [amrfinderplus.protein.aro.tsv](https://github.com/BigDataBiology/arg-compare/blob/676af9a0886234608b6c6ecd0c35da53d777ed3e/aro_normalization/amrfinderplus.protein.aro.tsv)
- Column specification
*'Protein identifier'* column is the GMGC unigene accession.
#### Run AMRFinderPlus command
```
amrfinder -p ${DIR}/${infile} --threads 64 -o ~/${infile}.tsv
```

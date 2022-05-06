# ARG-OAP ORF-mode

## Run hmmsearch 
Sargfam.hmm is downloaded from https://github.com/xiaole99/Sargfam

`run_hmmsearch.sh`
```
hmmsearch --cpu 64 --cut_ga --tblout arg_oap_result_GMGC.tsv Sargfam.hmm GMGC10.95nr.faa
#filter results
awk '$5 < 0.00001' arg_oap_result_GMGC.tsv >arg_oap_result_GMGC_filtered.tsv
```

## Hamronization and ARO mapping
`args_oap_hamronized_map_aro.py`

### Hamronization
Example:
If target reference name is "bacitracin__bacA_train_msa", then gene_symbol will be "bacA", gene_name will be "bacitracin__bacA", drug_class will be "bacitracin"

### ARO mapping
The *reference_database_id* & *gene symbol* & *gene_name* in `arg_oap_result_GMGC_filtered_hamronized.tsv` are inconsistant with *Original ID* & *Gene Name in CARD* in `resfinder_ncbi_sarg_resfinderfg_deeparg_ARO_mapping.txt`

Manually normalize sargfam name to make them consistant for ARO mapping.

Normalization reference is in `sargfam_name_normalization.xlsx`

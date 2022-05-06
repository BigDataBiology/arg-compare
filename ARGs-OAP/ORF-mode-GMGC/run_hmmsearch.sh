hmmsearch --cpu 64 --cut_ga --tblout arg_oap_result_GMGC.tsv Sargfam.hmm GMGC10.95nr.faa
awk '$5 < 0.00001' arg_oap_result_GMGC.tsv >arg_oap_result_GMGC_filtered.tsv
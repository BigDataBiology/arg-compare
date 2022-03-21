# reads mode
singularity exec -B /home/yiqian/AMR/ARG-OAP/inputdir /home/yiqian/AMR/ARG-OAP/argoapv2.5.sif /home/argsoapv2.5/argoap_version2.5 -i /home/yiqian/AMR/ARG-OAP/inputdir -m /home/yiqian/AMR/ARG-OAP/metadata.txt -o /home/yiqian/AMR/ARG-OAP/test_out -n 8 -z

# contig mode
hmmscan --cut_ga --tblout args_oap_hmm_result.tsv Sargfam.hmm GMGC10.wastewater.95nr.faa.gz
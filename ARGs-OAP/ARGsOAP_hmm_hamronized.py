def hamronized(infile,outfile):
    out = open(outfile,"wt")
    
    out.write(f"input_sequence_id\tinput_file_name\tgene_symbol\tgene_name\treference_database_id\treference_database_version\treference_accession\tanalysis_software_name\tanalysis_software_version\tsequence_identity\tinput_protein_start\tinput_protein_stop\tinput_gene_start\tinput_gene_stop\treference_protein_start\treference_protein_stop\treference_gene_start\treference_gene_stop\tstrand_orientation\tcoverage_depth\tcoverage_percentage\tcoverage_ratio\treference_gene_length\treference_protein_length\tinput_gene_length\tinput_protein_length\tdrug_class\tantimicrobial_agent\tresistance_mechanism\n")
    
    with open(infile,"rt") as f:
        for line in f:
            linelist = line.strip().split(" ")
            if line[0]!="#":
                for i in linelist:
                    if i.startswith("GMGC"):
                        input_sequence_id = i
                input_file_name = "GMGC10.wastewater.95nr.faa"
                gene_symbol = linelist[0].split("__")[1].split("_")[0]
                gene_name = linelist[0].replace("_train_msa","")
                reference_database_id = "SARG"
                reference_database_version = "2.0"
                reference_accession = linelist[0]
                analysis_software_name = "ARGs-OAP"
                analysis_software_version = "2.0"
                drug_class = linelist[0].split("__")[0]
                out.write(f"{input_sequence_id}\t{input_file_name}\t{gene_symbol}\t{gene_name}\t{reference_database_id}\t{reference_database_version}\t{reference_accession}\t{analysis_software_name}\t{analysis_software_version}\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{drug_class}\t\t\n")            
    out.close
                  

INPUT_FILE = "args_oap_hmm_result.tsv"
OUTPUT_FILE = "ARGsOAP_hmm_hamronized.tsv"        
hamronized(INPUT_FILE,OUTPUT_FILE)
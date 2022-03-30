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
                gene_name = linelist[0].replace("_train_msa","")
                gene_symbol = gene_name.split("__",1)[1]
                if gene_symbol == "aac_2___I":
                    gene_symbol = "aac(2')-I"
                if gene_symbol == "aac_3__I":
                    gene_symbol = "aac(3)-I"  
                if gene_symbol == "aac_3__II":
                    gene_symbol = "aac(3)-II"
                if gene_symbol == "aac_3__IV":
                    gene_symbol = "aac(3)-IV"                   
                if gene_symbol == "aac_6___31":
                    gene_symbol = "aac(6')-31"                    
                if gene_symbol == "ADP_ribosylating_transferase_arr":
                    gene_symbol = "ADP-ribosylating transferase_arr"
                if gene_symbol == "ant_2____I":
                    gene_symbol = "ant(2'')-I"
                if gene_symbol == "ant_3____Ih_aac_6___IId":
                    gene_symbol = "ant(3'')-Ih-aac(6')-IId"
                if gene_symbol == "aph_3____I":
                    gene_symbol = "aph(3'')-I"
                if gene_symbol == "aph_3___I":
                    gene_symbol = "aph(3')-I"
                if gene_symbol == "aph_3___IIb":
                    gene_symbol = "aph(3')-IIb" 
                if gene_symbol == "aph_3_____III":
                    gene_symbol = "aph(3''')-III" 
                if gene_symbol == "aph_4__I":
                    gene_symbol = "aph(4)-I" 
                if gene_symbol == "aph_6__I":
                    gene_symbol = "aph(6)-I" 
                if gene_symbol == "bicyclomycin_multidrug_efflux_protein_bcr":
                    gene_symbol = "bicyclomycin-multidrug_efflux_protein_bcr" 
                if gene_symbol == "cat_chloramphenicol_acetyltransferase":
                    gene_symbol = "cat_chloramphenicol acetyltransferase"   
                if gene_symbol == "CMY_2":
                    gene_symbol = "CMY-2" 
                if gene_symbol == "EmrB_QacA_family_major_facilitator_transporter":
                    gene_symbol = "EmrB-QacA family major facilitator transporter"    
                if gene_symbol == "kasugamycin_resistance_protein_ksgA":
                    gene_symbol = "kasugamycin resistance protein ksgA"    
                if gene_symbol == "OXA_119":
                    gene_symbol = "OXA-119"                 
                if gene_symbol == "PBP_1A":
                    gene_symbol = "PBP-1A"     
                if gene_symbol == "PBP_1B":
                    gene_symbol = "PBP-1B"
                if gene_symbol == "PBP_2X":
                    gene_symbol = "PBP-2X"
                if gene_symbol == "rifampin_monooxygenase":
                    gene_symbol = "rifampin monooxygenase"
                if gene_symbol == "SHV_5":
                    gene_symbol = "SHV-5"                    
                if gene_symbol == "streptothricin_acetyltransferase":
                    gene_symbol = "streptothricin acetyltransferase"   
                     
                reference_database_id = "sarg_db"
                reference_database_version = "2.0"
                reference_accession = linelist[0]
                analysis_software_name = "ARGs-OAP"
                analysis_software_version = "2.0"
                drug_class = linelist[0].split("__",1)[0]
                out.write(f"{input_sequence_id}\t{input_file_name}\t{gene_symbol}\t{gene_name}\t{reference_database_id}\t{reference_database_version}\t{reference_accession}\t{analysis_software_name}\t{analysis_software_version}\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{drug_class}\t\t\n")            
    out.close
                  

INPUT_FILE = "args_oap_hmm_result.tsv"
OUTPUT_FILE = "ARGsOAP_hmm_hamronized.tsv"        
hamronized(INPUT_FILE,OUTPUT_FILE)
def hamronized(infile,outfile):
    out = open(outfile,"wt")
    
    out.write(f"input_sequence_id\tinput_file_name\tgene_symbol\tgene_name\treference_database_id\treference_database_version\treference_accession\tanalysis_software_name\tanalysis_software_version\tsequence_identity\tinput_protein_start\tinput_protein_stop\tinput_gene_start\tinput_gene_stop\treference_protein_start\treference_protein_stop\treference_gene_start\treference_gene_stop\tstrand_orientation\tcoverage_depth\tcoverage_percentage\tcoverage_ratio\treference_gene_length\treference_protein_length\tinput_gene_length\tinput_protein_length\tdrug_class\tantimicrobial_agent\tresistance_mechanism\n")
    
    with open(infile,"rt") as f:
        for line in f:
            linelist = line.strip().split(" - ")
            if line[0]!="#":
                input_sequence_id = linelist[0].strip()
                input_file_name = "GMGC10.95nr.faa"
                gene_name = linelist[1].strip().replace("_train_msa","")
                gene_symbol = gene_name.split("__",1)[1]                     
                reference_database_id = "sarg_db"
                reference_database_version = "2.0"
                reference_accession = linelist[1].strip()
                analysis_software_name = "ARGs-OAP"
                analysis_software_version = "2.0"
                drug_class = linelist[1].strip().split("__",1)[0]
                out.write(f"{input_sequence_id}\t{input_file_name}\t{gene_symbol}\t{gene_name}\t{reference_database_id}\t{reference_database_version}\t{reference_accession}\t{analysis_software_name}\t{analysis_software_version}\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{drug_class}\t\t\n")            
    out.close
                  
def store_aro(infile):
    aro_dict = {}
    with open(infile,"rt") as f:
        for line in f:
            linelist = line.strip().split("\t")
            if len(linelist) == 5:
                if linelist[4] == "sarg":
                    aro_dict[linelist[2]] = linelist[3]
    return aro_dict

def map_aro(aro_dict,infile,outfile):   
    change_dict = {"aac_3__IIIa":"AAC(3)-IIIa","aac_3__IV":"AAC(3)-IV","aac_6___31":"AAC(6')-31",
                   "aadD":"ANT(4')-Ib","ADP_ribosylating_transferase_arr":"arr-2","ant_3____Ih_aac_6___IId":"aadA6/aadA10",
                   "aph_3___I":"APH(3')-Ia","aph_3___IIb":"APH(3')-IIb","CMY_2":"CMY-2","dfrA16":"DfrA37","ereA":"EreA",
                   "erm_38_":"Erm(38)","erm_41_":"Erm(37)","ermC":"ErmC","ermE":"ErmE","ermF":"ErmF",
                   "ermG":"ErmG","ermT":"ErmT","ermX":"ErmX","floR":"cmlA9","fmtC":"mprF",
                   "fosB":"FosB","fosX":"FosX","IMP_1":"IMP-1","IND_12":"IND-12","mdfA":"Escherichia coli mdfA",
                   "mexA":"MexA","mexB":"MexB","mexC":"MexC","mexD":"MexD","mexE":"MexE",
                   "mexF":"MexF","mexH":"MexH","mexW":"MexW","multidrug_ABC_transporter":"msbA","ompR":"CpxR",
                   "oprJ":"OprJ","oprN":"OprN","OXA_119":"OXA-119","OXA_46":"OXA-46","OXA_9":"OXA-9",
                   "qacG":"qacH","rifampin_monooxygenase":"iri","SHV_5":"SHV-5","streptothricin_acetyltransferase":"sta","tet34":"ErmU",
                   "tet40":"tet(40)","tetC":"tet(C)","tetE":"tet(E)","tetH":"tet(H)","tetJ":"tet(J)",
                   "tetL":"tet(L)","tetR":"MexL","tetV":"tet(V)","tetY":"tet(Y)","viomycin_phosphotransferase":"vph"}  
    
    out = open(outfile,"wt")
    out.write(f"input_sequence_id\tinput_file_name\tgene_symbol\tgene_name\treference_database_id\treference_database_version\treference_accession\tanalysis_software_name\tanalysis_software_version\tsequence_identity\tinput_protein_start\tinput_protein_stop\tinput_gene_start\tinput_gene_stop\treference_protein_start\treference_protein_stop\treference_gene_start\treference_gene_stop\tstrand_orientation\tcoverage_depth\tcoverage_percentage\tcoverage_ratio\treference_gene_length\treference_protein_length\tinput_gene_length\tinput_protein_length\tdrug_class\tantimicrobial_agent\tresistance_mechanism\tGene Name in CARD\tARO\tgene_symbol_short\tconfers_resistance_to_antibiotic\n")       
    
    with open(infile,"rt") as f:
        for line in f:
            if line[0] != "i":
                linelist = line[:-1].split("\t")
                if linelist[2] in change_dict.keys():
                    gene_symbol = change_dict[linelist[2]]
                    if gene_symbol in aro_dict.keys():
                        out.write(f'{line[:-1]}\t{gene_symbol}\tAR0:{aro_dict[gene_symbol]}\t\t\n')
                else:
                    gene_symbol = linelist[2]
                    if gene_symbol in aro_dict.keys():
                        out.write(f'{line[:-1]}\t{gene_symbol}\tARO:{aro_dict[gene_symbol]}\t\t\n')
                    else:
                        out.write(f'{line[:-1]}\t\t\t\t\n')

INPUT_FILE_1 = "arg_oap_result_GMGC_filtered.tsv"
INPUT_FILE_2 = "/resfinder_ncbi_sarg_resfinderfg_deeparg_ARO_mapping.txt"
OUTPUT_FILE_1 = "arg_oap_result_GMGC_filtered_hamronized.tsv"
OUTPUT_FILE_2 = "arg_oap_result_GMGC_filtered_hamronized_aro.tsv"
        
hamronized(INPUT_FILE_1,OUTPUT_FILE_1)
aro_dict = store_aro(INPUT_FILE_2)
map_aro(aro_dict,OUTPUT_FILE_1,OUTPUT_FILE_2)
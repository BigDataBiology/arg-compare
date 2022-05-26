'''
Nomalize gene_symbol based on subtype_hmm_sarg.xlsx from Xiaole and resfinder_ncbi_sarg_resfinderfg_deeparg_ARO_mapping.txt.
'''
def hamronized(infile,outfile):
    import gzip
    out = open(outfile,"wt")
    
    out.write(f"input_sequence_id\tinput_file_name\tgene_symbol\tgene_name\treference_database_id\treference_database_version\treference_accession\tanalysis_software_name\tanalysis_software_version\tsequence_identity\tinput_protein_start\tinput_protein_stop\tinput_gene_start\tinput_gene_stop\treference_protein_start\treference_protein_stop\treference_gene_start\treference_gene_stop\tstrand_orientation\tcoverage_depth\tcoverage_percentage\tcoverage_ratio\treference_gene_length\treference_protein_length\tinput_gene_length\tinput_protein_length\tdrug_class\tantimicrobial_agent\tresistance_mechanism\n")
    change_dict = {"aac_2___I":"aac(2')-I","aac_3__I":"aac(3)-I","aac_3__II":"AAC(3)-II","aac_3__IIIa":"AAC(3)-IIIa","aac_3__IV":"AAC(3)-IV","aac_3__VIII":"AAC(3)-VIIIa","aac_6___31":"AAC(6')-31",
                   "aadD":"ANT(4')","aadE":"ANT(6)","ADP_ribosylating_transferase_arr":"arr-2","ant_2____I":"ANT(2'')-Ia","ant_3____Ih_aac_6___IId":"aadA6/aadA10","aph_3_____III":"APH(3')-IIIa",
                   "aph_3____I":"aph(3'')-I","aph_3___I":"aph(3')-I","aph_3___IIb":"APH(3')-IIb","aph_4__I":"aph(4)-I","aph_6__I":"aph(6)-I","bicyclomycin_multidrug_efflux_protein_bcr":"bcr-1","catB":"Clostridium butyricum catB","cmlA":"Escherichia coli mdfA","CMY_2":"CMY-2","ereA":"EreA",
                   "erm_38_":"Erm(38)","erm_41_":"Erm(41)","ermC":"ErmC","ermE":"ErmE","ermF":"ErmF",
                   "ermG":"ErmG","ermT":"ErmT","ermX":"ErmX","fmtC":"Listeria monocytogenes mprF",
                   "fosB":"FosB","fosX":"FosX","IMP_1":"IMP-1","IND_12":"IND-12","mdfA":"Escherichia coli mdfA","mefA":"mel",
                   "mexA":"MexA","mexB":"MexB","mexC":"MexC","mexD":"MexD","mexE":"MexE",
                   "mexF":"MexF","mexH":"MexH","mexW":"MexW","OKP_A":"OKP-A","OKP_B":"OKP-B","omp36":"Klebsiella aerogenes Omp36","ompF":"porin OmpF",
                   "oprJ":"OprJ","oprN":"OprN","OXA_119":"OXA-119","OXA_46":"OXA-46","OXA_9":"OXA-9","OXY_1":"OXY-1","OXY_2":"OXY-2","PBP_1A":"Streptococcus pneumoniae PBP1a conferring resistance to amoxicillin","PBP_1B":"PBP-1B","PBP_2X":"Streptococcus pneumoniae PBP2x conferring resistance to amoxicillin",
                   "qepA":"QepA1","rifampin_monooxygenase":"rifampin monooxygenase","SHV_5":"SHV-5","streptothricin_acetyltransferase":"sta",
                   "tet40":"tet(40)","tetC":"tet(C)","tetE":"tet(E)","tetH":"tet(H)","tetJ":"tet(J)",
                   "tetL":"tet(L)","tetV":"tet(V)","tetY":"tet(Y)","viomycin_phosphotransferase":"vph"}  
        
    with gzip.open(infile,"rt") as f:
        for line in f:
            linelist = line.strip().split(" - ")
            if line[0]!="#":
                input_sequence_id = linelist[0].strip()
                input_file_name = "GMGC10.95nr.faa"
                gene_name = linelist[1].strip().replace("_train_msa","")
                gene_symbol = gene_name.split("__",1)[1]                
                if gene_symbol in change_dict.keys():
                    gene_symbol = change_dict[gene_symbol]
                reference_database_id = "sarg_db"
                reference_database_version = "2.3"
                reference_accession = linelist[1].strip()
                analysis_software_name = "ARGs-OAP"
                analysis_software_version = "2.3"
                drug_class = linelist[1].strip().split("__",1)[0]
                out.write(f"{input_sequence_id}\t{input_file_name}\t{gene_symbol}\t{gene_name}\t{reference_database_id}\t{reference_database_version}\t{reference_accession}\t{analysis_software_name}\t{analysis_software_version}\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{drug_class}\t\t\n")            
    out.close()

'''
Store ARO number of each gene_symbol based on resfinder_ncbi_sarg_resfinderfg_deeparg_ARO_mapping.txt.
Add ARO number of gene_symbol that searched in CARD manually.
'''    
def store_aro(infile):
    aro_dict = {"AAC(3)-VIIIa":"3002542","ANT(4')":"3000229","ANT(6)":"3000225","ANT(2'')-Ia":"3000230",
                "APH(3')-IIIa":"3002647","Clostridium butyricum catB":"3002674","dfrA16":"3003014","emrD":"3000309","emrE":"3000264",
                "Erm(41)":"3000603","ermB":"3000375","floR":"3002705","FosA":"3000149","marR":"3000718","mdtK":"3001327","mdtL":"3001215",
                "mexT":"3000814","mtrR":"3000817","Klebsiella aerogenes Omp36":"3003385","porin OmpF":"3000265","Streptococcus pneumoniae PBP1a conferring resistance to amoxicillin":"3003041",
                "Streptococcus pneumoniae PBP2x conferring resistance to amoxicillin":"3003043","qacG":"3007015","QepA1":"3000448",
                "rifampin monooxygenase":"3000445","tcmA":"3003554","tet34":"3002870","tetR":"3003479","vanH":"3000006","vanR":"3000574",
                "vanS":"3000071","vanT":"3000372","vanW":"3000002","vanX":"3000011","vanY":"3000077","vanZ":"3000116"}
    with open(infile,"rt") as f:
        for line in f:
            linelist = line.strip().split("\t")
            if len(linelist) == 5:
                if linelist[4] == "sarg":
                    aro_dict[linelist[2]] = linelist[3]
    return aro_dict

'''
Map ARO number based on gene_symbol.
'''
def map_aro(aro_dict,infile,outfile):   
    out = open(outfile,"wt")
    out.write(f"input_sequence_id\tinput_file_name\tgene_symbol\tgene_name\treference_database_id\treference_database_version\treference_accession\tanalysis_software_name\tanalysis_software_version\tsequence_identity\tinput_protein_start\tinput_protein_stop\tinput_gene_start\tinput_gene_stop\treference_protein_start\treference_protein_stop\treference_gene_start\treference_gene_stop\tstrand_orientation\tcoverage_depth\tcoverage_percentage\tcoverage_ratio\treference_gene_length\treference_protein_length\tinput_gene_length\tinput_protein_length\tdrug_class\tantimicrobial_agent\tresistance_mechanism\tGene Name in CARD\tARO\tgene_symbol_short\tconfers_resistance_to_antibiotic\n")       
    
    with open(infile,"rt") as f:
        for line in f:
            if line[0] != "i":
                linelist = line[:-1].split("\t")
                gene_symbol = linelist[2]
                if gene_symbol in aro_dict.keys():
                    out.write(f'{line[:-1]}\t{gene_symbol}\tAR0:{aro_dict[gene_symbol]}\t\t\n')
                else:
                    out.write(f'{line[:-1]}\t\t\t\t\n') 
             
INPUT_FILE_1 = "arg_oap_result_GMGC_filtered.tsv.gz"
INPUT_FILE_2 = "resfinder_ncbi_sarg_resfinderfg_deeparg_ARO_mapping.txt"
OUTPUT_FILE_1 = "arg_oap_result_GMGC_filtered_hamronization.tsv"
OUTPUT_FILE_2 = "arg_oap_result_GMGC_filtered_hamronization_aro.tsv"
        
hamronized(INPUT_FILE_1,OUTPUT_FILE_1)
aro_dict = store_aro(INPUT_FILE_2)
map_aro(aro_dict,OUTPUT_FILE_1,OUTPUT_FILE_2)
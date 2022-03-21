def hamronized(infile1,infile2,outfile):
    out = open(outfile,"wt") 
    out.write(f"input_sequence_id\tinput_file_name\tgene_symbol\tgene_name\treference_database_id\treference_database_version\treference_accession\tanalysis_software_name\tanalysis_software_version\tsequence_identity\tinput_protein_start\tinput_protein_stop\tinput_gene_start\tinput_gene_stop\treference_protein_start\treference_protein_stop\treference_gene_start\treference_gene_stop\tstrand_orientation\tcoverage_depth\tcoverage_percentage\tcoverage_ratio\treference_gene_length\treference_protein_length\tinput_gene_length\tinput_protein_length\tdrug_class\tantimicrobial_agent\tresistance_mechanism\n")
    gene_type = {}
        
    with open(infile1,"rt") as f1:
        for line in f1:
            Gene,Subtype,Type,sample1,sample2 = line.strip().split("\t")
            gene_type[Gene] = Type
    
    with open(infile2,"rt") as f2:
        for line in f2:
            qseqid,sseqid,pident,length,mismatch,gapopen,qstart,qend,sstart,send,evalue,bitscore = line.strip().split("\t")
            out.write(f"{qseqid}\t\t{sseqid}\t{sseqid}\tSARG\t2.3\t{sseqid}\tARGs-OAP\t2.3\t{pident}\t\t\t{qstart}\t{qend}\t\t\t{sstart}\t{send}\t\t\t\t\t\t\t\t\t{gene_type[sseqid]}\t\t\n")
            
    out.close
                  
INPUT_FILE_1 = "stage2output.normalize_cellnumber.gene.txt"
INPUT_FILE_2 = "args_oap_reads_result.tsv"
OUTPUT_FILE = "ARGsOAP_reads_hamronized.tsv"        
hamronized(INPUT_FILE_1,INPUT_FILE_2,OUTPUT_FILE)
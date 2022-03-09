def hamronized(infile1,infile2,infile3,outfile):
    out = open(outfile,"wt") 
    gene_type = {}
    
    with open(infile1,"rt") as f1:
        title = f1.readline()
        out.write(title)
        
    with open(infile2,"rt") as f2:
        for line in f2:
            Gene,Subtype,Type,sample1,sample2 = line.strip().split("\t")
            gene_type[Gene] = Type
    
    with open(infile3,"rt") as f3:
        for line in f3:
            qseqid,sseqid,pident,length,mismatch,gapopen,qstart,qend,sstart,send,evalue,bitscore = line.strip().split("\t")
            out.write(f"{qseqid}\t\t{sseqid}\t{sseqid}\tSARG\t\t{sseqid}\tARGs-OAP\t\t{pident}\t\t\t{qstart}\t{qend}\t\t\t{sstart}\t{send}\t\t\t\t\t\t\t\t\t{gene_type[sseqid]}\t\t\n")
            
    out.close
                  
INPUT_FILE_1 = "combined_hamronized_report.tsv"
INPUT_FILE_2 = "stage2output.normalize_cellnumber.gene.txt"
INPUT_FILE_3 = "stage2output.blast6out2.txt"
OUTPUT_FILE = "ARGsOAP_hamronized.txt"        
hamronized(INPUT_FILE_1,INPUT_FILE_2,INPUT_FILE_3,OUTPUT_FILE)
import re   

def haplo_parse(input_string):
    '''
    Takes input string in bp format (output from ped-sim) and returns a list of dictionaries containing chromosome number, haplotype,
    block length and [start, stop] positions as keys 
    
    '''
    
    input_string = input_string.replace('\n',' ') #Replace trailing newline with a space for easier regex processing
    parsed_list = re.findall(r'(\d{1,2}\|\d+\s(?:\d+:\d+\s)+)', input_string, re.MULTILINE) #Killer regex here. 

    haplo_lists_of_dicts = [None]*len(parsed_list)
    
    for i in range(len(parsed_list)): #Loop over the chromosomes
        #regex parse each list entry to pull out all the information we need 
        chrom = re.search(r'^[^|]*',parsed_list[i]).group(0)
        chrom_start = int(re.search(r'\|(.*?)\s', parsed_list[i]).group(1))
        haplotypes = re.findall(r'\s(.*?):', parsed_list[i]) 
        chrom_end_list = re.findall(r':(.*?)\s', parsed_list[i])
        range_list = [[int(chrom_start),int(chrom_end_list[i])]  if i==0 else [int(chrom_end_list[i-1]),int(chrom_end_list[i])] for i in range(len(chrom_end_list))]
        chrom_list = [{'haplotypes':haplotypes[j] ,'startstop':range_list[j], 'chromosome':chrom, 'length':range_list[j][1] - range_list[j][0] } for j in range(len(haplotypes)) ] 
        haplo_lists_of_dicts[i] = chrom_list # Assign chromosome i's list of haplotype dictionaries to a list 
    
    haplo_dicts = [item for sublist in haplo_lists_of_dicts for item in sublist] #Collapse list 
    return(haplo_dicts) 



# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:24:02 2018

@author: Alex Malokin
"""

import sys
import os 
import csv



#add or increase counters within a dictionary
#@param key: a key to test whether it exists in the dictionary
#@param dct: a dictionary to test the key
#@value: increases the key count by 1
def add_to_dict(key, dct):
    if key in dct:
        dct[key] += 1
    else:
        dct[key] = 1

#read dataset and produce counter dictionaries
#@param path: path to the dataset
#@value: a tuple of counter dictionaries (occupation, state)
def input_reader(path):   
    #init dictionaries of counters
    occ_dict = {}
    state_dict = {}
    
    #read first record of the csv file to determine keys
	#coult be expanded/modified if keys change in future
    with open(path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        row1 = next(csv_reader)
        #key for status
        if 'STATUS' in row1:
            status_key = 'STATUS'
        elif 'CASE_STATUS' in row1:
            status_key = 'CASE_STATUS'
        #key for occupation name
        if 'LCA_CASE_SOC_NAME' in row1:
            soc_name_key = 'LCA_CASE_SOC_NAME'
        elif 'SOC_NAME' in row1:
            soc_name_key = 'SOC_NAME'
        #key for state    
        if 'LCA_CASE_WORKLOC1_STATE' in row1:
            st_name_key = ('LCA_CASE_WORKLOC1_STATE',
                           'LCA_CASE_WORKLOC2_STATE')
        elif 'WORKSITE_STATE' in row1:
            st_name_key = ('WORKSITE_STATE',) * 2
         
    #read csv file
    with open(path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')        
        for row in csv_reader:
            if row[status_key] == "CERTIFIED": #only process a cert. record
                #counter for occupations
                add_to_dict(row[soc_name_key], occ_dict)
                #counter for states, which accounts for 2 locations
                state_name = (row[st_name_key[0]],
                              row[st_name_key[1]])  
                if state_name[0]: #loc1 is not missing
                    add_to_dict(state_name[0], state_dict)                 
                else: #loc1 is missing
                    if state_name[1]: #loc2 is not missing
                        add_to_dict(state_name[1], state_dict)
                        
    return (occ_dict, state_dict)

#sort counter dicitionaries and calculate shares for each key
#@param dct: dictionary with counters
#@value: sorted list of tuples (key, count, share)
def share_calc(dct):
    #sort into list: count(D), name(A)
    sorted_list = sorted(dct.items(), 
                      key=lambda x: (-x[1], x[0]))
    #get the total
    list_total = sum(dct.values())
    #add shares to the sorted list
    list_shares = [(key, value, ("{:.1%}".format(value / list_total))) 
                    for key, value in sorted_list]  
    
    return list_shares

#write output files
#@param output_list: sorted list with keys, counts, and shares
#@param file_name: filename for the output
#@param header: which header in the output file to use -  
#               ("occ", "state") for occupations and states, respectively
#@param n: how many top keys to include in the output, if number of keys is lower than n
#		all keys are outputted
#@value: creates outputfiles in the ../output folder
def output_writer(output_list, file_name, header="occ", n=10):
    with open(file_name, mode='w') as out_file:
        txt_writer = csv.writer(out_file, delimiter=';')
        if header == "occ":
            txt_writer.writerow(["TOP_OCCUPATIONS", "NUMBER_CERTIFIED_APPLICATIONS", "PERCENTAGE"])
        elif header == "state":
            txt_writer.writerow(["TOP_STATES", "NUMBER_CERTIFIED_APPLICATIONS", "PERCENTAGE"])
        for i in range(min(n, len(output_list))):
            txt_writer.writerow(output_list[i])



if __name__ == "__main__":
    
    #locate input folder
    #input_folder = os.path.join("input")
    #set path to the input dataset
    #dataset_path = os.path.join(input_folder, sys.agrv[1])
    #locate output folder
    #output_folder = os.path.join("output")
    #set paths to the output files
    #output_path_occ = os.path.join(output_folder, "top_10_occupations.txt")
    #output_path_state = os.path.join(output_folder, "top_10_states.txt")
    
    #read input data and generate counter dictionaries
    occ_counters, state_counters = input_reader(sys.argv[1])
    #calculate shares
    occ_shares = share_calc(occ_counters)
    state_shares = share_calc(state_counters)
    
    #write output files
    output_writer(occ_shares, sys.argv[2], "occ", 10)
    output_writer(state_shares, sys.argv[3], "state", 10)

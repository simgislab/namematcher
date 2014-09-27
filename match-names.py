#!/usr/bin/env python -u
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# match-names.py
# Author: Maxim Dubinin (sim@gis-lab.info)
# About: For each input name search for reference name and add associated codes to the output.
# Created: 24.03.2014
# Usage example: python match-names.py in.csv ref.csv out.csv
# ---------------------------------------------------------------------------


import sys
import csv

def prepare_in_name(in_name):

    res = in_name.upper()
    res = res.replace(u"Ё",u"Е")

    return res

def prepare_ref_name(ref_name):

    res = ref_name.upper()
    res = res.replace(u"Ё",u"Е")

    return res

if __name__ == '__main__':
    args = sys.argv[ 1: ]
    f_in_name = args[0]
    f_ref_name = args[1]
    f_out_name = args[2]

    f_in = open(f_in_name)
    fieldnames_data = {"NAME"}
    csv_in = csv.DictReader(f_in, fieldnames=fieldnames_data)

    f_ref = open(f_ref_name)
    fieldnames_data = {"NUM","NAME","AO","TYPE","OKATO","OKTMO"}
    csv_ref = csv.DictReader(f_ref)

    f_out = open(f_out_name,"wb")
    fieldnames_data = {"NAME","REF_NAME","OKATO"}
    csv_out = csv.DictWriter(f_out, fieldnames=fieldnames_data)

    #prepare input and ref arrays
    in_names_prep = []
    ref_names = []
    ref_names_prep = []
    ref_codes = []
    
    for reg in csv_ref:
        ref_names.append(reg['NAME'].decode('utf-8'))
        ref_names_prep.append(prepare_ref_name(reg['NAME'].decode('utf-8')))
        ref_codes.append(reg['OKATO'])

    in_count = 0
    found_count = 0
    for reg in csv_in:
        in_count = in_count + 1
        in_name = reg['NAME'].decode('utf-8')

        #prepare matching string
        in_name_prep = prepare_in_name(reg['NAME'].decode('utf-8'))

        #find a match
        ref_code = ""
        ref_name_select = ""

        #search if there are any matches
        matches = [s for s in ref_names_prep if s in in_name_prep]

        #if there is just one match - get it
        if len(matches) == 1:
            ind = ref_names_prep.index(matches[0])
            ref_name_select = ref_names[ind]
            ref_code = ref_codes[ind]
            #write to output
            csv_out.writerow(dict(NAME=in_name.encode('utf-8'),
                                  REF_NAME=ref_name_select.encode('utf-8'),
                                  OKATO=ref_code))
            found_count = found_count + 1
        elif len(matches) > 1: #there may be multiple finds, select the best (longest) match
            for match in matches:
                ind = ref_names_prep.index(max(matches,key=len))
                ref_name_select = ref_names[ind]
                ref_code = ref_codes[ind]

                #write to output
                csv_out.writerow(dict(NAME=in_name.encode('utf-8'),
                                      REF_NAME=ref_name_select.encode('utf-8'),
                                      OKATO=ref_code))
                found_count = found_count + 1
                break
        else:   #nothing found, write input as it is
            csv_out.writerow(dict(NAME=in_name.encode('utf-8'),
                                      REF_NAME=ref_name_select.encode('utf-8'),
                                      OKATO=ref_code))
            
    print("Found: " + str(found_count) + " out of " + str(in_count))

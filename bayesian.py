#!/usr/bin/python

"""%prog [--help] [LM dir] [input file] [output file]

This project builds a naïve Bayesian classifier that will classify text fragments and list the most probable language.
"""

import sys
import glob
import math

def create_input_tuple(lines) -> dict:
    input_list_of_tuples = []
    for line in lines:
        splitline = line.split('\t')
        langcode = splitline[0]
        langtext = splitline[1]
        langtuple = (langcode,langtext)
        input_list_of_tuples.append(langtuple)

    return input_list_of_tuples

def create_lm_dictionary(lm_lines) -> dict:
    language_count = {}
    for line in lm_lines:
        splitcount = line.split('\t')
        word = splitcount[0]
        count = splitcount[1].strip('\n')
        language_count[word] = count
       
    return language_count

def calculate_probability(inputtext, lm_models) -> dict:
    probability_dict = {}
    for modelkey in lm_models:
        # Count total number of words in a language model
        totalwords = 0
        for word in lm_models[modelkey]:
            totalwords = totalwords + int(lm_models[modelkey][word])
        
        # Calculate the probability for the words in the input text
        lang_probability = 0
        for word in inputtext:
            if word in lm_models[modelkey]:
                word_probability = (int(lm_models[modelkey][word]) / totalwords)               
            else:
                word_probability = (int(lm_models[modelkey]["<UNK>"]) / totalwords)
            lang_probability = lang_probability + math.log10(word_probability)
        probability_dict[modelkey] = round(lang_probability, 6)
    
    return probability_dict        
    
def main():
    lm_dir = sys.argv[1]
    lm_files = glob.glob(lm_dir + '/*')
    inputfile = sys.argv[2]
    outputfile = sys.argv[3]
    
    # Read in text to classify and create input dictionary
    with open(inputfile, 'r', encoding='utf8') as f: 
        inputlines = f.readlines()
    input_tuples = create_input_tuple(inputlines)
    
    # Read in the unigrams and counts for each language model
    lm_dictionary = {}
    for filename in lm_files:  
        with open(filename, 'r', encoding='utf8') as f: 
            lm_words = f.readlines()     
        name = filename.split('/')[-1]
        lang_code = name[:3]
        lm_dictionary[lang_code] = create_lm_dictionary(lm_words)

    with open(outputfile, 'w', encoding='utf8') as f: 
        # For each list entry in the input tuple
        for i in input_tuples:
            f.write(i[0] + '\t' + i[1])
            text_to_analyze = i[1].split()
            probabilities = calculate_probability(text_to_analyze,lm_dictionary)
            best_score = 0
            sorted(probabilities.keys())
            for key in sorted(probabilities.keys()) :
                f.write(key + "\t" + str(probabilities[key]) + '\n')
                
            max_prob = list(probabilities.values())
            max_key = list(probabilities.keys())
            f.write("result" + '\t' + max_key[max_prob.index(max(max_prob))] + '\n') 
            f.write('\n')

if __name__ == "__main__":
    main()
    
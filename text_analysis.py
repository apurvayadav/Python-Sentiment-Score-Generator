# Importing Packages

import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import re
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')

#Creating stop words list after downloading text file from giving URL
stop_words_list = []
with open("StopWords_Generic.txt", encoding="utf-8") as f:
    for line in f:
        stripped_line = line.strip('\n')
        stop_words_list.append(stripped_line)

#Opening master dict obtained from given URL's master degree.
#To make this word_data.xlsx MS excel's filters are used.
master_dict = pd.read_excel("word_data.xlsx", engine="openpyxl")

#for the output results
output_dict = {"POSITIVE SCORE" : [],
    "NEGATIVE SCORE": [], 
    "POLARITY SCORE": [],	
    "SUBJECTIVITY SCORE": [],	
    "AVG SENTENCE LENGTH": [],	
    "PERCENTAGE OF COMPLEX WORDS":[],	
    "FOG INDEX": [],	
    "AVG NUMBER OF WORDS PER SENTENCE": [],	
    "COMPLEX WORD COUNT": [],	
    "WORD COUNT": [],	
    "SYLLABLE PER WORD": [],	
    "PERSONAL PRONOUNS": [],	
    "AVG WORD LENGTH": []
    }
#defining fumction for text preprocessing
def preprocessing(file):
    data = []
    raw_data = file
    raw_data = data.append(raw_data)

    #converting text to lowercase
    clean_text = []
    for words in data:
            clean_text.append(str.lower(words))

    #creating word and sentence tokens from the nltk's tokenize module
    word_tok = [ word_tokenize(i) for i in clean_text]
    sent_tok = [sent_tokenize(i) for i in clean_text]

    #removing punctuations from the word tokens using regex
    clean_text_1 = []
    import re
    for words in word_tok:
        clean = []
        for w in words:
            res = re.sub(r'[^\w\s]',"",w)
            if res != "":
                clean.append(res)
            clean_text_1.append(clean)

    #removing stopwords from the word tokens
    clean_text_2 = []
    for words in clean_text_1:
        w = []
        for word in words:
            if not word in stop_words_list:
                w.append(word)
            clean_text_2.append(w)
    
    #for reference
    print("preprocessing done")

    return clean_text_2, sent_tok


# defining function forntext analysis on the two lists obtained from the preprocessing function.
def text_analysis(final_word_tok, sent_tok):
    
    #Positive Score: This score is calculated by assigning the value of +1 for each word
    # if found in the Positive Dictionary and then adding up all the values.
    positive_score = 0
    for word in list(master_dict.positive):
            if word in final_word_tok[0]:
                positive_score += final_word_tok[0].count(word)
    output_dict["POSITIVE SCORE"].append(positive_score)

    # Negative Score: This score is calculated by assigning the value of -1 for each word if found in the Negative Dictionary 
    # and then adding up all the values. We multiply the score with -1 so that the score is a positive number.
    negative_score = 0
    for word in list(master_dict.negative):
        if word in final_word_tok[0]:
            negative_score += final_word_tok[0].count(word)
    output_dict["NEGATIVE SCORE"].append(negative_score)

    #Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)
    polarity_score = (positive_score - negative_score)/((positive_score + negative_score) + 0.000001)
    output_dict["POLARITY SCORE"].append(polarity_score)

    #Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)
    subjectivity_score = (positive_score + negative_score)/( (len(final_word_tok[0]) + 0.000001))
    output_dict["SUBJECTIVITY SCORE"].append(subjectivity_score)

    # Complex words are words in the text that contain more than two syllables.
    no_of_complex_words = 0
    for word in list(master_dict.complex):
        if word in final_word_tok[0]:
            no_of_complex_words += final_word_tok[0].count(word)
    output_dict["COMPLEX WORD COUNT"].append(no_of_complex_words)

    # Percentage of Complex words = the number of complex words / the number of words 
    percentage_of_complex_words = (no_of_complex_words / len(final_word_tok[0]))*100
    output_dict["PERCENTAGE OF COMPLEX WORDS"].append(percentage_of_complex_words)

    # Average Sentence Length = the number of words / the number of sentences
    average_sent_len = len(final_word_tok[0]) / len(sent_tok[0])
    output_dict["AVG SENTENCE LENGTH"].append(average_sent_len)

    #Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)
    fog_index = 0.4 * (average_sent_len + percentage_of_complex_words)
    output_dict["FOG INDEX"].append(fog_index)

    #Average Number of Words Per Sentence = the total number of words / the total number of sentences
    average_no_of_words_per_sent = len(final_word_tok[0]) / len(sent_tok[0])
    output_dict["AVG NUMBER OF WORDS PER SENTENCE"].append(average_no_of_words_per_sent)

    #We count the total cleaned words present in the text by 
    # 1.	removing the stop words (using stopwords class of nltk package).
    # 2.	removing any punctuations like ? ! , . from the word before counting.

    clean_text_4 = []
    w = []
    for word in final_word_tok[0]:
        if not word in stopwords.words('english'):
            w.append(word)
        clean_text_4.append(w)
    output_dict["WORD COUNT"].append(len(clean_text_4[0]))

    #We count the number of Syllables in each word of the text by counting the vowels present in each word.
    # We also handle some exceptions like words ending with "es","ed" by not counting them as a syllable.
    n_vowel = 0
    vowels = ["a", "e", "i", "o", "u"]
    for word in final_word_tok[0]:
        if not (word.endswith("es") or word.endswith("ed") ):
            for vowel in vowels:
                if vowel in word:
                    n_vowel += word.count(vowel)
    output_dict["SYLLABLE PER WORD"].append(n_vowel/len(final_word_tok[0]))

    #To calculate Personal Pronouns mentioned in the text, we use regex to find the counts of the words
    #  - “I,” “we,” “my,” “ours,” and “us”. 
    # Special care is taken so that the country name US is not included in the list.
    pp = ["i", "we", "ours", "us"]
    pp_count = 0
    for word in final_word_tok[0]:
        for p in pp:
            if word == p:
                pp_count += 1
    output_dict["PERSONAL PRONOUNS"].append(pp_count)

    #Average Word Length is calculated by the formula:
    # Sum of the total number of characters in each word/Total number of words
    average_word_length = 0
    for word in final_word_tok[0]:
        average_word_length += len(word)
    output_dict["AVG WORD LENGTH"].append(average_word_length/len(final_word_tok[0]))

    print("analysis done")
    
    return output_dict            

import os
i = 1
for filename in os.listdir("text_files"):
    with open(os.path.join("text_files", filename), 'r', encoding='utf-8') as f:
        file = f.read()

    final_word_tok, sent_tok = preprocessing(file)
    output_dict = text_analysis(final_word_tok, sent_tok)
    print(f"analysis done for {i+1}.txt") #for reference
    i += 1
    

# making dataframe of output file
df = pd.DataFrame(output_dict)

#input file
input = pd.read_excel("Input.xlsx", engine="openpyxl")
input = input.iloc[:, [0,1]]

#combining for final csv
final_output = pd.concat([input, df], axis=1)

#creating final csv
final_output.to_csv("Output.csv", index=False)
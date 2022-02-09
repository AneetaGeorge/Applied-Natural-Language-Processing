import sys
import glob
import math
import re
import json
import os


def preprocess(input):
    input = input.rstrip('\n')
    input = input.lower()
    input = remove_punct(input)
    input = remove_stop_words(input)

    return input

def remove_punct(input):
    #input = input.translate(str.maketrans('', '', string.punctuation))
    input = re.sub(r'[^\w\s]','',input)
    return input

def remove_stop_words(input):
    input.strip()
    #stop_words =  ["a", "i", "im", "that", "this", "which", "is", "are", "the", "at", "in", "and", "to", "my", "it", "he", "of", "they", "for", "when", "an", "you", "me", "on",
     #               "what", "", "his", "will", "about", "after", "our", "your", "yours", "youre", "their", "theirs", "there", "where", "here", "theres", "her", "was", "is", "are",
      #              "be", "so", "would", "from"]
    stop_words = []

    list = []

    for word in input.split(" "):
        if(word not in stop_words):
            list.append(word)
    return list


test_path = str(sys.argv[1]) + '/*/*/*/*.txt'
model_path = "nbmodel.txt"
model = json.load(open(model_path))

txt_files = glob.glob(test_path)
f = open('nboutput.txt', 'w')

for txt_file in txt_files:

        #file_split = os.path.normpath(txt_file)
        #file_split  = file_split .split(os.sep)

        #np_label = file_split[-4].lower()
        #td_label = file_split[-3].lower()

        #file_name = txt_file.split("\\")[-1]

        file_handle = open(txt_file, "r")
        input = file_handle.read()
        input = preprocess(input)

        p_positive = 0
        p_negative = 0
        p_truthful = 0
        p_deceptive = 0 

        for word in input:
            p_positive += math.log(model['positive'].get(word, 1)) - math.log(model.get('positive-count', 1))
            p_negative += math.log(model['negative'].get(word, 1)) - math.log(model.get('negative-count', 1))
            p_truthful += math.log(model['truthful'].get(word, 1)) - math.log(model.get('truthful-count', 1))
            p_deceptive += math.log(model['deceptive'].get(word, 1)) - math.log(model.get('deceptive-count', 1))

        result = ""

        if(p_truthful > p_deceptive):
            result += "truthful"
        else:
            result += "deceptive"

        result += " "

        if(p_positive > p_negative):
            result += "positive"
        else:
            result += "negative"

        result += " " + txt_file + "\n"

        f.write(result)
        
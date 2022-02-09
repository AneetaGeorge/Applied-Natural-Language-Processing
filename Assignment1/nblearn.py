import sys
import re
import glob
import json

input_path = str(sys.argv[1])

model = {}

deceptive = {}
truthful = {}

negative = {}
positive = {}

vocabulary = set()

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
    #stop_words =["a", "i", "im", "that", "this", "which", "is", "are", "the", "at", "in", "and", "to", "my", "it", "he", "of", "they", "for", "when", "an", "you", "me", "on",
         #           "what", "", "his", "will", "about", "after", "our", "your", "yours", "youre", "their", "theirs", "there", "where", "here", "theres", "her", "was", "is", "are",
              #      "be", "so", "would", "from"]
    stop_words = []

    list = []

    for word in input.split(" "):
        if(word not in stop_words):
            list.append(word)
    return list


def create_dict(txt_files, dict1, dict2):

    count = 0
    for txt_file in txt_files:

        file_handle = open(txt_file, "r")
        input = file_handle.read()
        input = preprocess(input)

        for word in input:
            dict1[word] = dict1.get(word, 1) + 1
            dict2[word] = dict2.get(word, 1) + 1
            count += 1
            vocabulary.add(word)
            

    return count

txt_files = glob.glob(input_path + '/positive_polarity/deceptive*/*/*.txt')
count = create_dict(txt_files, positive, deceptive)
model['positive-count'] = model.get('positive-count', 0) + count
model['deceptive-count'] = model.get('deceptive-count', 0) + count

txt_files = glob.glob(input_path + '/positive_polarity/truthful*/*/*.txt')
count = create_dict(txt_files, positive, truthful)
model['positive-count'] = model.get('positive-count', 0) + count
model['truthful-count'] = model.get('truthful-count', 0) + count

txt_files = glob.glob(input_path + '/negative_polarity/deceptive*/*/*.txt')
count = create_dict(txt_files, negative, deceptive)
model['negative-count'] = model.get('negative-count', 0) + count
model['deceptive-count'] = model.get('deceptive-count', 0) + count

txt_files = glob.glob(input_path + '/negative_polarity/truthful*/*/*.txt')
count = create_dict(txt_files, negative, truthful)
model['negative-count'] = model.get('negative-count', 0) + count
model['truthful-count'] = model.get('truthful-count', 0) + count

model['positive-count'] = model.get('positive-count', 0) + len(vocabulary)
model['negative-count'] = model.get('negative-count', 0) + len(vocabulary)
model['truthful-count'] = model.get('truthful-count', 0) + len(vocabulary)
model['deceptive-count'] = model.get('deceptive-count', 0) + len(vocabulary)

model['positive'] = positive
model['negative'] = negative
model['truthful'] = truthful
model['deceptive'] = deceptive

json.dump(model, open("nbmodel.txt",'w'))


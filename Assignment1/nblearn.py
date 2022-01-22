from os import read
import sys
import string
import glob

input_path = str(sys.argv[1])

def preprocess(input):
    input = input.rstrip('\n')
    input = input.lower()
    input = remove_punct(input)
    input = remove_stop_words(input)

    return input

def remove_punct(input):
    input = input.translate(str.maketrans('', '', string.punctuation))
    return input

def remove_stop_words(input):
    input.strip()
    return input

deceptive = {}
truthful = {}

negative = {}
positive = {}

def create_dict(txt_files, dict1, dict2):

    count = 0
    for txt_file in txt_files:

        file_handle = open(txt_file, "r")
        input = file_handle.read()
        input = preprocess(input)
        for word in input.split(" "):
            dict1[word] = dict1.get(word, 0) + 1
            dict2[word] = dict2.get(word, 0) + 1
        count += 1

txt_files = glob.glob(input_path + '/positive_polarity/deceptive*/*/*.txt')
create_dict(txt_files, positive, deceptive)

txt_files = glob.glob(input_path + '/positive_polarity/truthful*/*/*.txt')
create_dict(txt_files, positive, truthful)

txt_files = glob.glob(input_path + '/negative_polarity/deceptive*/*/*.txt')
create_dict(txt_files, negative, deceptive)

txt_files = glob.glob(input_path + '/negative_polarity/truthful*/*/*.txt')
create_dict(txt_files, negative, truthful)

model = {}

model['positive'] = positive
model['negative'] = negative
model['truthful'] = truthful
model['deceptive'] = deceptive

target = open('nbmodel.txt', 'a')
target.write(str(model))

print(negative)

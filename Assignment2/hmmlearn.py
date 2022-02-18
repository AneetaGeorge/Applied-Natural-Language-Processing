import sys
import json


def write_to_file(model):
    json.dump(model, open('hmmmodel.txt', 'w', encoding='utf-8'))


def learn_hmm_model(train_file):
    hmm_model = {'tag-count': {}, 'tag-bigram-count': {}, 'word-tag-count': {}, 'tag-tag-count': {}}

    with open(train_file, 'r', encoding='utf-8') as fh:
        lines = fh.readlines()

    for line in lines:
        line = line.rstrip()
        prev_tag = ''

        for word_tag in line.split(" "):
            word, tag = word_tag.rsplit("/", 1)
            word = word.lower()

            # Update dicionary with word-tag and tag-tag counts
            if word not in hmm_model['word-tag-count']:
                hmm_model['word-tag-count'][word] = {}

            hmm_model['word-tag-count'][word][tag] = hmm_model['word-tag-count'][word].get(tag, 0) + 1
            hmm_model['tag-count'][tag] = hmm_model['tag-count'].get(tag, 0) + 1

            if prev_tag not in hmm_model['tag-tag-count']:
                hmm_model['tag-tag-count'][prev_tag] = {}

            hmm_model['tag-tag-count'][prev_tag][tag] = hmm_model['tag-tag-count'][prev_tag].get(tag, 0) + 1
            hmm_model['tag-bigram-count'][prev_tag] = hmm_model['tag-bigram-count'].get(prev_tag, 0) + 1

            prev_tag = tag

    return hmm_model

# Read the input file from command line argument and learn the HMM model


input_file = sys.argv[-1]
model = learn_hmm_model(input_file)
write_to_file(model)

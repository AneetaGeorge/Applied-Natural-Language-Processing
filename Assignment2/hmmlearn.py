import sys
import json


def write_to_file(model):
    json.dump(model, open('hmmmodel.txt', 'w', encoding='utf-8'))


def learn_hmm_model(train_file):
    hmm_model = {'tag-count': {}, 'tag-bigram-count': {}, 'tag-word-count': {}, 'tag-tag-count': {}}

    with open(train_file, 'r', encoding='utf-8') as fh:
        lines = fh.readlines()

    for line in lines:
        line = line.rstrip()
        prev_tag = ''

        for word_tag in line.split(" "):
            word, tag = word_tag.rsplit("/", 1)

            # if len(word_split) == 2:
            #     word, tag = word_split[0], word_split[1]
            # elif len(word_split) == 3:
            #     word = '/'
            #     tag = word_split[-1]
            # else:
            #     continue

            # Update dicionary with word-tag and tag-tag counts

            if tag not in hmm_model['tag-word-count'].keys():
                hmm_model['tag-word-count'][tag] = {}

            hmm_model['tag-word-count'][tag][word] = hmm_model['tag-word-count'][tag].get(word, 0) + 1
            hmm_model['tag-count'][tag] = hmm_model['tag-count'].get(tag, 0) + 1

            if prev_tag not in hmm_model['tag-tag-count'].keys():
                hmm_model['tag-tag-count'][prev_tag] = {}

            hmm_model['tag-tag-count'][prev_tag][tag] = hmm_model['tag-tag-count'][prev_tag].get(tag, 0) + 1
            hmm_model['tag-bigram-count'][prev_tag] = hmm_model['tag-bigram-count'].get(prev_tag, 0) + 1

            prev_tag = tag

    return hmm_model

# Read the input file from command line argument and learn the HMM model


input_file = sys.argv[-1]
model = learn_hmm_model(input_file)
write_to_file(model)

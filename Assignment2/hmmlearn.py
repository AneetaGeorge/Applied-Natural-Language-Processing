import sys
import json


def write_to_file(model):
    json.dump(model, open('hmmmodel.txt', 'w', encoding='utf-8'))


def learn_hmm_model(train_file):
    hmm_model = {'tag-count': {}, 'tag-bigram-count': {}, 'word-tag-count': {}, 'tag-tag-count': {}}
    tag_vocabulary_set = {}
    vocabulary = set()
    open_class_vocab_threshold_percent = 0.025

    with open(train_file, 'r', encoding='utf-8') as fh:
        lines = fh.readlines()

    for line in lines:
        line = line.rstrip()
        prev_tag = ''

        for word_tag in line.split(" "):
            word, tag = word_tag.rsplit("/", 1)
            word = word.lower()

            vocabulary.add(word)

            # Update dicionary with word-tag and tag-tag counts
            if word not in hmm_model['word-tag-count']:
                hmm_model['word-tag-count'][word] = {}

            hmm_model['word-tag-count'][word][tag] = hmm_model['word-tag-count'][word].get(tag, 0) + 1
            hmm_model['tag-count'][tag] = hmm_model['tag-count'].get(tag, 0) + 1

            if prev_tag not in hmm_model['tag-tag-count']:
                hmm_model['tag-tag-count'][prev_tag] = {}

            if tag not in tag_vocabulary_set:
                tag_vocabulary_set[tag] = set()

            tag_vocabulary_set[tag].add(word)

            hmm_model['tag-tag-count'][prev_tag][tag] = hmm_model['tag-tag-count'][prev_tag].get(tag, 0) + 1
            hmm_model['tag-bigram-count'][prev_tag] = hmm_model['tag-bigram-count'].get(prev_tag, 0) + 1

            prev_tag = tag

    open_class_vocab_threshold = open_class_vocab_threshold_percent * len(vocabulary)

    hmm_model['open-class-tags'] = [tag for tag, vocab_set in tag_vocabulary_set.items()
                                    if len(vocab_set) > open_class_vocab_threshold]

    hmm_model['vocabulary-len'] = len(vocabulary)

    return hmm_model


# Read the input file from command line argument and learn the HMM model


input_file = sys.argv[-1]
model = learn_hmm_model(input_file)
write_to_file(model)

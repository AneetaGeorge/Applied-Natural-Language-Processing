import sys
import json


def backtrack(back_pointer, last_state, index):

    tag_sequence = []
    while last_state != '':
        tag_sequence.insert(0, last_state)
        last_state = back_pointer[last_state][index]
        index -= 1

    return tag_sequence


def write_to_file(result, filename):
    with open(filename, 'w', encoding='utf-8') as fh:
        fh.write(result)


def transition_probability(model, tag1, tag2):

    if tag1 not in model['tag-tag-count']:
        trans_prob = 0.01
        pass
    else:
        if tag2 not in model['tag-tag-count'][tag1]:
            trans_prob = 0.01
        else:
            trans_prob = model['tag-tag-count'][tag1][tag2] / model['tag-bigram-count'].get(tag1, 1)

    return trans_prob


def emission_probability(model, tag, word):
    word = word.lower()
    if word in model['word-tag-count']:
        emission_prob = model['word-tag-count'][word].get(tag, 0) / model['tag-count'].get(tag, 1)
    else:
        emission_prob = 1

    return emission_prob


def is_unknown_word(model, word):
    word = word.lower()

    if word in model['word-tag-count']:
        return False

    return True


def viterbi_decode(hmm_model, sentence):
    tags = hmm_model['tag-count'].keys()
    open_tags = hmm_model['open-class-tags']
    tag_probability = {}
    back_pointer = {}
    max_prev_tag = ''

    considered_tags = tags

    for tag in considered_tags:
        if tag not in tag_probability:
            tag_probability[tag] = {}

        if tag not in back_pointer:
            back_pointer[tag] = {}

        tag_probability[tag][0] = transition_probability(hmm_model, '', tag) * emission_probability(hmm_model, tag, sentence[0])
        back_pointer[tag][0] = ''

    for t in range(1, len(sentence)):
        if is_unknown_word(hmm_model, sentence[t]):
            considered_tags = open_tags
        else:
            considered_tags = tags

        for tag in considered_tags:
            emission_prob = emission_probability(hmm_model, tag, sentence[t])
            max_prob = 0

            if is_unknown_word(hmm_model, sentence[t - 1]):
                prev_considered_tags = open_tags
            else:
                prev_considered_tags = tags

            for prev_tag in prev_considered_tags:
                trans_prob = transition_probability(hmm_model, prev_tag, tag)

                curr_prob = tag_probability[prev_tag][t - 1] * trans_prob

                if max_prob < curr_prob:
                    max_prob = curr_prob
                    max_prev_tag = prev_tag

            tag_probability[tag][t] = max_prob * emission_prob
            back_pointer[tag][t] = max_prev_tag  # Check if this is the correct prev tag

    last_state = len(sentence) - 1
    max_prob = 0
    most_probable_end_state = ''

    for tag in tags:
        if last_state in tag_probability[tag]:
            curr_prob = tag_probability[tag][last_state] * trans_prob
        else:
           continue
        if max_prob < curr_prob:
            max_prob = curr_prob
            most_probable_end_state = tag

    return backtrack(back_pointer, most_probable_end_state, last_state)
    pass


def pos_tag_sentences(test_file):

    pos_tagged_sentences = ''
    with open(test_file, 'r', encoding='utf-8') as fh:
        lines = fh.readlines()

    for line in lines:
        line = line.rstrip()
        words = line.split(" ")
        tag_sequence = viterbi_decode(hmm_model, words)

        for i in range(len(words)):
            pos_tagged_sentences += words[i] + "/" + tag_sequence[i] + " "
            pass
        pos_tagged_sentences += '\n'

    return pos_tagged_sentences


def read_model_from_file(model_path):
    with open(model_path, encoding='utf-8') as fh:
        model = json.load(fh)
    return model


test_file = sys.argv[-1]
hmm_model = read_model_from_file("hmmmodel.txt")
pos_tag_result = pos_tag_sentences(test_file)
write_to_file(pos_tag_result, 'hmmoutput.txt')

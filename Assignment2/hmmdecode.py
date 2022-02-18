import sys
import json


def backtrack(back_pointer, last_state, index):
    # print(last_state)
    tag_sequence = []
    # tag_sequence.append(last_state)
    while last_state != '':
        # print(back_pointer[last_state])
        tag_sequence.insert(0, last_state)
        last_state = back_pointer[last_state][index]
        index -= 1

    print(tag_sequence)
    return tag_sequence


def write_to_file(result, filename):
    with open(filename, 'w', encoding='utf-8') as fh:
        fh.write(result)


def transition_probability(model, tag1, tag2):
    trans_prob = model['tag-tag-count'][tag1].get(tag2, 0.01) / model['tag-bigram-count'].get(tag1, 1)
    # print(trans_prob)
    return trans_prob


def emission_probability(model, tag, word):
    emission_prob = model['tag-word-count'][tag].get(word, 0) / model['tag-count'].get(tag, 0)
    return emission_prob


def viterbi_hmm(hmm_model, sentence):
    tags = hmm_model['tag-word-count'].keys()
    tag_probability = {}
    back_pointer = {}
    max_prev_tag = ''

    for tag in tags:
        if tag not in tag_probability.keys():
            tag_probability[tag] = {}

        if tag not in back_pointer.keys():
            back_pointer[tag] = {}

        tag_probability[tag][0] = transition_probability(hmm_model, '', tag) * emission_probability(hmm_model, tag, sentence[0])
        back_pointer[tag][0] = ''

    for t in range(1, len(sentence)):
        for tag in tags:
            max_prob = 0
            emission_prob = emission_probability(hmm_model, tag, sentence[t])
            if 0 == emission_probability(hmm_model, tag, sentence[t]):
                tag_probability[tag][t] = 0

                for prev_tag in tags:
                    curr_prob = tag_probability[prev_tag][t - 1] \
                                * transition_probability(hmm_model, prev_tag, tag)

                    if max_prob < curr_prob:
                        max_prob = curr_prob
                        max_prev_tag = prev_tag
                back_pointer[tag][t] = max_prev_tag

                # What will be back_pointer[tag][t] here??
            else:
                max_prob = 0
                for prev_tag in tags:
                    trans_prob = transition_probability(hmm_model, prev_tag, tag)
                    # print(trans_prob, emission_prob)
                    curr_prob = tag_probability[prev_tag][t - 1] * trans_prob

                    # print(curr_prob)
                    if max_prob < curr_prob:
                        max_prob = curr_prob
                        max_prev_tag = prev_tag
                # print(max_prev_tag)
                tag_probability[tag][t] = max_prob * emission_prob
                back_pointer[tag][t] = max_prev_tag  # Check if this is the correct prev tag

    last_state = len(sentence) - 1
    max_prob = 0
    most_probable_end_state = ''

    for tag in tags:
        if max_prob < tag_probability[tag][last_state]:
            max_prob = tag_probability[tag][last_state]
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
        # viterbi_hmm(hmm_model, words)
        tag_sequence = viterbi_hmm(hmm_model, words)

        for i in range(len(words)):
            pos_tagged_sentences += words[i] + "/" + tag_sequence[i] + " "
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

'''
This file takes tokenized and tagged tweets from an input file
and builds an arff datafile that can be used to train models
and classify tweets. Takes 3 arguments:

1. input filename
2. output filename
3. (optional) max number twts from *each* class that is used
'''

import os
import sys
import math
import header
import wordlist


def count_tags(input, tags):
    '''
    Counts the number of tokens with the given tags.
    :param input: str
    :param tag: list
    :return: int
    '''
    if len(input) == 0:
        return 0
    total = 0
    sentences = input.split('\n')
    for sent in sentences:
        words = sent.split()
        for word in words:
            if word.split('/')[-1] in tags:     # safe split index
                total += 1
    return total


def split_word(word):
    '''
    Splits words safely by / character
    :param word:
    :return:
    '''
    w = word.split('/')
    if len(w) > 2:
        return "/".join(w[0:-1]), w[-1]
    return w[0], w[1]


def first_person_pronoun(input):
    '''
    Counts the number of first person pronouns.
    valid = I, me, my, mine, we, us, our, ours
    :param input:
    :return:
    '''
    if len(input) == 0:
        return 0

    total = 0
    sentences = input.split('\n')
    for sent in sentences:
        words = sent.split()
        for word in words:
            [w, tag] = split_word(word)
            if w.lower() in wordlist.FPP:
                total += 1
    return total


def second_person_pronoun(input):
    '''
    Counts the number of second person pronouns.
    valid = you, your, yours, u, ur, urs
    :param input:
    :return:
    '''
    if len(input) == 0:
        return 0

    total = 0
    sentences = input.split('\n')
    for sent in sentences:
        words = sent.split()
        for word in words:
            [w, tag] = split_word(word)
            if w.lower() in wordlist.SPP:
                total += 1
    return total


def third_person_pronoun(input):
    '''
    Counts number of third person pronouns.
    valid = he, him, his, she, her, hers, it, its, they, them, their, theirs
    :param input:
    :return:
    '''
    if len(input) == 0:
        return 0

    total = 0
    sentences = input.split('\n')
    for sent in sentences:
        words = sent.split()
        for word in words:
            [w, tag] = split_word(word)
            if w.lower() in wordlist.TPP:
                total += 1
    return total


def coordinating_conjunctions(input):
    '''
    valid = tokens tagged as CC
    :param input:
    :return:
    '''
    return count_tags(input, ['CC'])


def past_tense_verbs(input):
    '''
    valid = tagged as VBD
    :param input:
    :return:
    '''
    return count_tags(input, ['VBD'])


def future_tense_verbs(input):
    '''
    valid = 'll, will, gonna, going + to + VB
    :param input: str
    :return: int
    '''
    if len(input) == 0:
        return 0

    total = 0
    sentences = input.split('\n')
    for sent in sentences:
        words = sent.split()
        for i, word in enumerate(words):
            [w, tag] = split_word(word)
            if w.lower() in ["'ll", "will", "gonna"]:
                total += 1
            elif w.lower() == "going" and i < len(words) - 2 and words[i + 1].split('/')[0].lower() == "to" \
                and words[i + 2].split('/')[1] == "VB":
                total += 1
    return total


def commas(input):
    '''
    valid = ,
    :param input:
    :return:
    '''
    return count_tags(input, [','])


def colons(input):
    '''
    valid = ; and :
    :param input: str
    :return: int
    '''
    if len(input) == 0:
        return 0

    total = 0
    sentences = input.split('\n')
    for sent in sentences:
        words = sent.split()
        for word in words:
            [w, tag] = split_word(word)
            if tag == ":" and w in [";", ":"]:
                total += 1
    return total


def dashes(input):
    '''
    valid = - and -- only, longer dashes not recognized
    :param input:
    :return:
    '''
    if len(input) == 0:
        return 0

    total = 0
    sentences = input.split('\n')
    for sent in sentences:
        words = sent.split()
        for word in words:
            [w, tag] = split_word(word)
            if tag == ":" and w.count("-") > 0:
                total += 1
    return total


def parentheses(input):
    '''
    valid = ( and ) and [ and ] and { and }
    :param input:
    :return:
    '''
    return count_tags(input, ["(", ")"])


def ellipse(input):
    '''
    valid = any number of periods greater than 1
    :param input:
    :return:
    '''
    if len(input) == 0:
        return 0

    total = 0
    sentences = input.split('\n')
    for sent in sentences:
        words = sent.split()
        for word in words:
            [w, tag] = split_word(word)
            if tag == ":" and w.count(".") > 0:
                total += 1
            elif tag == "CD" and w.count(".") > 3:  # longer ellipses get tagged as CD for some reason
                total += 1
    return total


def common_nouns(input):
    '''
    valid = tagged as NN, NNS
    :param input:
    :return:
    '''
    return count_tags(input, ['NN', 'NNS'])


def proper_nouns(input):
    '''
    valid = tagged as NNP, NNPS
    :param input:
    :return:
    '''
    return count_tags(input, ['NNP', 'NNPS'])


def adverbs(input):
    '''
    valid = tagged as RB, RBR, RBS
    :param input:
    :return:
    '''
    return count_tags(input, ['RB', 'RBR', 'RBS'])


def wh_words(input):
    '''
    valid = WDT, WP, WP$, WRB
    :param input:
    :return:
    '''
    return count_tags(input, ['WDT', 'WP', 'WP$', 'WRB'])


def modern_slang_acronyms(input):
    '''
    valid = smh, fwb, lmfao, lmao, lms, tbh, rofl, wtf, bff, wyd, lylc, brb, atm, imao, sml, btw,
    bw, imho, fyi, ppl, sob, ttyl, imo, ltr, thx, kk, omg, ttys, afn, bbs, cya, ez, f2f, gtr,
    ic, jk, k, ly, ya, nm, np, plz, ru, so, tc, tmi, ym, ur, u, sol, lol
    added = omfg, fml, lmk
    :param input: str
    :return: int
    '''
    if len(input) == 0:
        return 0

    sentences = input.split('\n')
    total = 0
    for sent in sentences:
        words = sent.split()
        for word in words:
            [w, tag] = split_word(word)
            if w.lower() in wordlist.SLANG:
                total += 1
    return total


def uppercase_words(input):
    '''
    valid = any word longer than 1 letter that is all uppercase
    :param input:
    :return:
    '''
    if len(input) == 0:
        return 0

    sentences = input.split('\n')
    total = 0
    for sent in sentences:
        words = sent.split()
        for word in words:
            [w, tag] = split_word(word)
            if len(w) > 1 and w.isupper():
                total += 1
    return total


def avg_sentence_length(input):
    '''
    Average sentence length, in tokens.
    :param input: str
    :return: int
    '''
    if len(input) == 0:
        return 0

    sentences = input.split('\n')
    num_s = len(sentences)
    num_t = 0

    for sent in sentences:
        num_t += len(sent.split())

    return math.floor(num_t / num_s)


def avg_token_length(input):
    '''
    Average token length, in letters. Excludes punctuation tokens.
    :param input:
    :return:
    '''
    if len(input) == 0:     # avoid zero division error
        return 0

    sentences = input.split('\n')
    total = 0
    tokens = 0
    for sent in sentences:
        words = sent.split()
        for word in words:
            [w, tag] = split_word(word)
            # sometimes !!! and ??? and other variations get tagged as nouns
            if tag not in wordlist.PUNCTUATION and not (tag == 'NN' and (w.count('!') or w.count('?'))):
                tokens += 1
                total += len(w)

    return math.floor(total / tokens)


def num_sentences(input):
    '''
    Returns the number of sentences.
    :param input: str
    :return: int
    '''
    return input.count('\n')


def build_arff_file(raw_in, out_file, max_sent):
    '''
    Main function for handling counting.
    :param raw_in:
    :param out_file:
    :param max_sent:
    :return:
    '''
    if os.path.exists(out_file):
        os.remove(out_file)

    fh = open(out_file, 'wb')
    fh.write(header.HEADER)

    tweets = raw_in.split("<A=")
    sent_count = {'0': 0, '4': 0}

    for t in tweets:
        if not t:           # empty line
            continue

        sentiment = t[0]    # keep track of each type
        if sent_count[sentiment] >= max_sent:
            continue
        sent_count[sentiment] += 1

        tweet = t[3:]
        if tweet == '':     # empty tweets also count
            fh.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,{}".format(sentiment))
            continue

        fpp = first_person_pronoun(tweet)
        spp = second_person_pronoun(tweet)
        tpp = third_person_pronoun(tweet)
        cc = coordinating_conjunctions(tweet)
        ptv = past_tense_verbs(tweet)
        ftv = future_tense_verbs(tweet)
        comma = commas(tweet)
        colon = colons(tweet)
        dash = dashes(tweet)
        pare = parentheses(tweet)
        ell = ellipse(tweet)
        com_n = common_nouns(tweet)
        prop_n = proper_nouns(tweet)
        adv = adverbs(tweet)
        wh = wh_words(tweet)
        slang = modern_slang_acronyms(tweet)
        upper = uppercase_words(tweet)
        s_len = avg_sentence_length(tweet)
        t_len = avg_token_length(tweet)
        s_num = num_sentences(tweet)
        fh.write("\n{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
            fpp, spp, tpp, cc, ptv, ftv, comma, colon, dash, pare, ell, com_n, prop_n, adv,
            wh, slang, upper, s_len, t_len, s_num, sentiment))

    fh.close()

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Not enough arguments!")
    #     exit()
    #
    # if len(sys.argv) == 3:
    #     max = min(sys.argv[2], 10000)
    # else:
    #     max = 10000

    # file_in = sys.argv[0]
    # file_out = sys.argv[1]
    file_in = "twts.txt"
    file_out = "train.arff"
    max_ = 10000

    fh = open(file_in, 'r')
    raw_t = fh.read()

    build_arff_file(raw_t, file_out, max_)



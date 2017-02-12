'''
This file preprocesses the tweets by doing the following:
1. Remove all html tags and attributes
2. Replace html character codes with ASCII equivalent
3. Remove URLs
4. Remove @ and # before hashtags and usernames
5. Put each sentence in a tweet on its own line
7. Separate each token (incl punctuation and clitics) by a space
8. Tags each token with its PoS
9. Demarcate each tweet with its numeric class (on its own line in front)

Each of these tasks is its own function.

Note:
6. Leave ellipsis and multiple punctuation alone
2. If tweet is empty after preprocessing, that's fine
3. Don't split periods in abbreviations (such as e.g.)
4. Do whatever with hyphens
'''

import NLPlib
import sys
import csv
import pickle
import re
import HTMLParser
import os
import wordlist

tagger = NLPlib.NLPlib()
parser = HTMLParser.HTMLParser()

def demarcate_twt(input, polarity):
    '''

    :param input:
    :return:
    '''
    if polarity != '0' and polarity != '4':
        return("Error")

    return "<A={}>\n".format(polarity) + input


def tag_tokens(input):
    '''
    Tags the tokens with their PoS, task 7.
    :param input: 1D list of tokens in order
    :return: list of tags in the same order
    '''
    global tagger
    sentences = []
    for sent in input.strip().split("\n"):
        tokens = sent.strip().split()
        tags = tagger.tag(tokens)
        tag_sent = []
        for i, tag in enumerate(tags):
            tag_sent.append(tokens[i] + "/" + tag)
        sentences.append(" ".join(tag_sent))

    return "\n".join(sentences)


def separate_tokens(input):
    '''
    Separate each token by a space.
    :param input:
    :return:
    '''
    if len(input) == 0:
        return ""

    # simple method first
    sentences = input.strip().split('\n')
    sent = []
    for sentence in sentences:
        words = sentence.strip().split()
        clitics = ["'ve", "'m", "'s", "'d", "n't", "'ll", "s'"] # include possessive s' in clitics for convenience
        punctuation = re.compile(r'[)(\{\}\[\]]+|[\-]{2,1000}|[,]+|[!|?]+|[.]+|[:|;]+|[~]+|["]+|[/]+')
        # don't care about single dashes

        res = []
        for word in words:
            for clitic in clitics:  # check clitics next
                if clitic in word:
                    spl = word.split(clitic)
                    res.append(spl[0])
                    res.append(clitic)
                    word = spl[1]

            p = punctuation.search(word)
            while p:
                if word.lower() in wordlist.ABBREV:
                    p = None
                    continue
                start = p.start()
                end = p.end()
                # if word[start:end] == "," and word[start-1].isdigit() and word[end].isdigit():
                #     p = punctuation.search(word[end:])
                #     continue
                res.extend([word[0:start], word[start:end]])    # assumes no other punctuation
                word = word[end:]
                p = punctuation.search(word)

            res.append(word)

        sent.append(" ".join(res))

    return "\n".join(sent)


def insert_newline(index, input):
    '''
    Does the actual newline insertion
    :param indices:
    :param input:
    :return:
    '''
    new = ""
    for i in range(len(index)):
        if not i: continue
        if index[i] != index[-1]:
            new = new + input[index[i - 1]:index[i]] + "\n"
        else:
            new = new + input[index[i - 1]:index[i]]
    return new


def twt_to_sentences(input):
    '''
    Insert newlines between perceived sentences.
    :param input:
    :return:
    '''

    if len(input) == 0:
        return ""

    # define some regex expressions
    period = re.compile(
        r'(\.)+(?!\.)'       # ignore ellipses
    )
    excl = re.compile(
        r'(\?|!)(?=[^?!])'   # ignore multiple exclamation marks
    )
    other = re.compile(
        r'(;|:)+(?=.)'
    )

    # match periods
    # TODO: case with preceding known abbreviation (refer to textbook)
    index = [0] # keep track of the indices where newlines should go
    m = period.finditer(input)
    for p in m:
        end = p.end()
        # case with quotation marks, switch period and quote positions
        if input[end - 2] != "." and len(input) > end and (input[end] == '"' or input[end] == "'"):
            input = input[0:end - 1] + input[end] + input[end - 1] + input[end + 1:]
            index.append(end + 1)
        else:
            index.append(end)
    if index[-1] != len(input):
        index.append(len(input))
    input = insert_newline(index, input)

    # match question and exclamation marks
    index = [0]
    m = excl.finditer(input)
    for p in m:
        end = p.end()
        # case with quotation marks
        if (input[end - 2] != "!" and input[end - 2] != "?") and (input[end] == '"' or input[end] == "'"):
            input = input[0:end - 1] + input[end] + input[end - 1] + input[end + 1:]
            index.append(end + 1)
        else:
            index.append(end)
    if index[-1] != len(input):
        index.append(len(input))
    input = insert_newline(index, input)

    # match other
    index = [0]
    m = other.finditer(input)
    for p in m:
        index.append(p.end())
    if index[-1] != len(input):
        index.append(len(input))
    input = insert_newline(index, input)

    return input


def remove_at_hash(input):
    '''
    Removes the @ and # characters which precede usernames
    and hashtags in tweets.
    :param input:
    :return:
    '''

    if len(input) == 0:
        return ""

    # usernames are 1-15 chars only
    # does not match emails
    at_regex = re.compile(
        r'(?:^|\s)@(?P<name>[A-Za-z0-9_]{1,15})'
    )
    hash_regex = re.compile(
        r'(?:^|\s)#(?P<name>[A-Za-z0-9_]+)'
    )

    match = at_regex.search(input)
    while match:
        input = re.sub('@' + match.group('name'), match.group('name'), input)
        match = at_regex.search(input)

    match = hash_regex.search(input)
    while match:
        input = re.sub('#' + match.group('name'), match.group('name'), input)
        match = at_regex.search(input)

    return input

def remove_urls(input):
    '''
    Removes URLs.
    :param input:
    :return:
    '''

    if len(input) == 0:
        return ""

    # modified from http://daringfireball.net/2010/07/improved_regex_for_matching_urls
    url_regex = re.compile(
        r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>]))')
    # mods:
    # removed non-ascii characters from end of regex expression

    return url_regex.sub("", input)



def html_to_ascii(input):
    '''
    Converts HTML character codes to their ASCII equivalents.
    :param input:
    :return:
    '''

    if len(input) == 0:
        return ""

    # html parser library fails on some characters, such as french accents
    global parser
    # throw away characters that don't conform to ascii standard
    dec = input.decode('ascii', 'ignore')
    return parser.unescape(dec)


def remove_html(input):
    '''
    Strips html tags, attributes, chars
    :param input: tweets in a flat list
    :return: raw tweets containing no html items, in a flat list
    '''

    if len(input) == 0:
        return ""

    # Very basic
    twt_tags = re.sub("&gt;", ">", input)
    twt_tags = re.sub("&lt;", "<", twt_tags)

    return re.sub("<[^>]+>", '', twt_tags)


def preprocess(raw, polarities):
    '''
    Main function for preprocessing. Calls all other
    subfunctions.
    :param raw: raw tweets, in a flat list
    :return: processed and tagged tweets, in a flat list
    '''

    if len(raw) == 0:
        return ""

    res = []
    for i, twt in enumerate(raw):
        print(twt)
        no_html = remove_html(twt.strip())
        ascii = html_to_ascii(no_html)
        no_url = remove_urls(ascii)
        no_mentions = remove_at_hash(no_url)
        sent = twt_to_sentences(no_mentions)
        tokens = separate_tokens(sent)
        tagged = tag_tokens(tokens)
        demarcate = demarcate_twt(tagged, polarities[i])
        res.append(demarcate)

    return "\n".join(res)

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Error, not enough arguments!")
    #     exit()

    # X = 1000084981 % 80
    # fh = open("training.1600000.processed.noemoticon.csv", 'rb')
    #
    # # X = int(sys.argv[1]) % 80
    # # first section
    # bound1_low = X*10000 - 1
    # bound1_hi = X*10000 + 10000
    # # second section
    # bound2_low = 800000 + X*10000 - 1
    # bound2_hi = 800000 + X*10000 + 10000
    #
    # raw_tweets = []
    #
    # # open and read the file
    # #fh = open(sys.argv[0], 'rb')
    # reader = csv.reader(fh)
    # for i, line in enumerate(reader):
    #     if (i > bound1_low) and (i < bound1_hi):
    #         raw_tweets.append(line[0])
    #     if (i > bound2_low) and (i < bound2_hi):
    #         raw_tweets.append(line[0])
    # fh.close()

    # f = open('pols.pkl', 'wb')
    # pickle.dump(raw_tweets, f)
    f = open('twts.pkl', 'rb')
    raw_tweets = pickle.load(f)
    f.close()
    f = open('pols.pkl', 'rb')
    polarities = pickle.load(f)
    f.close()

    result = preprocess(raw_tweets, polarities)

    filename = "twts.txt"
    if os.path.exists(filename):
        os.remove(filename)

    fh = open(filename, 'wb')
    fh.write(result)
    fh.close()
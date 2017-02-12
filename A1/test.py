import re
import HTMLParser
import twtt
import random


l = [2, 3, 4, 5]
g = l[0, 1]


input = "i.e. hi there"
length = len(input)

input = "hi!,,,...--[there]"
punctuation = re.compile(r'[)(\{\}\[\]]+|[\-]{2,1000}|[,]+|[!|?]+|[.]+|[:|;]+|[~]+|["]+|[/]+')
b = punctuation.findall(input)


b = twtt.remove_at_hash(input)


period = re.compile(
    r'(\.)+(?!\.)'  # ignore ellipses
)
excl = re.compile(
    r'(\?|!)(?=[^?!])'  # ignore multiple exclamation marks
)
other = re.compile(
    r'(;|:)'
)

# match periods
index = [0]
m = period.finditer(input)
for p in m:
    end = p.end()
    # case with quotation marks
    if input[end - 2] != "." and (input[end] == '"' or input[end] == "'"):
        input = input[0:end - 1] + input[end] + input[end - 1] + input[end + 1:]
        index.append(end+1)
        l = input[end+1]
    elif end != len(input):
        index.append(end)
index.append(len(input))
new = ""
for i in range(len(index)):
    if not i: continue
    if index[i] != index[-1]:
        new = new + input[index[i-1]:index[i]] + "\n"
    else:
        new = new + input[index[i-1]:index[i]]
input = new

# match question and exclamation marks
m = excl.finditer(input)
for p in m:
    end = p.end()
    blah = input[end]
    # case with quotation marks
    if (input[end - 3] != "!" and input[end - 3] != "?") and (input[end - 1] == '"' or input[end - 1] == "'"):
        i = input[0:end - 2]
        input = input[0:end - 2] + input[end - 1] + input[end - 2] + "\n" + input[end:]
    else:
        input = input[0:end - 1] + "\n" + input[end - 1:]

# match other
m = other.finditer(input)
for p in m:
    end = p.end()
    input = input[0:end] + "\n" + input[end:]

words = input.split('\n')
punctuation = re.compile(
    r'[,|!|\?|.|:|;|-|~|"|\']+'
)
clitics = ["'ve", "'m", "'s", "'d", "n't"]
word = "tired!!!$10,000"
p = punctuation.finditer(word)
for i in p:
    start = i.start()
    end = i.end()
    new = word[0:start]
    n = word[start:end]
    l = word[end:]


print(input)
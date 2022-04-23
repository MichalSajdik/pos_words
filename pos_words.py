import requests
import nltk
from word2number import w2n

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
fp = open("text.txt")
data = fp.read()
# print('\n-----\n'.join(tokenizer.tokenize(data)))
sentences = tokenizer.tokenize(data)

splitSentences = []
splitPosSentences = []

for sentence in sentences:
    splitPosSentence = []
    splitSentence = []

    words = sentence.split()
    for word in words:
        if not word[len(word) - 1].isalpha():
            if not word.isnumeric():
                word = word[:len(word) - 1]

        r2 = requests.get('https://www.dictionary.com/browse/' + word)

        definitionString = '''<div class="css-69s207 e1hk9ate3"><span class="css-1b1gas3 e1hk9ate2"><span class="luna-pos">'''
        foundDefinitionString = r2.text.find(definitionString)
        if foundDefinitionString == -1:
            definitionString = '''<div class="css-69s207 e1hk9ate3"><span class="css-1b1gas3 e1hk9ate2"><span class="pos">'''
            foundDefinitionString = r2.text.find(definitionString)

        aa = foundDefinitionString + len(definitionString)
        bb = r2.text.find("<", aa)
        res = r2.text[aa:bb]
        c_type = ""
        if "article" in res:
            c_type = "DET"
        else:
            if res.find(" ") > -1:
                res = res[:res.find(" ")]
            if res.find(",") > -1:
                res = res[:res.find(",")]
            match res:
                case "adjective":
                    c_type = "ADJ"
                case "adj.":
                    c_type = "ADJ"
                case "adverb":
                    c_type = "ADV"
                case "conjunction":
                    c_type = "CNJ"
                case "auxiliary verb":
                    c_type = "MOD"
                case "noun":
                    c_type = "N"
                case "abbreviation":
                    c_type = "N"
                case "abbr.":
                    c_type = "N"
                case "n.":
                    c_type = "N"
                case "pl":  # pl n
                    c_type = "N"
                case "pronoun":
                    c_type = "PRO"
                case "preposition":
                    c_type = "P"
                case "interjection":
                    c_type = "UH"
                case "verb":
                    c_type = "V"
                case _:
                    c_type = res
                    # ""
                    # "NOPE"

        # if word.isnumeric():
        #     c_type = "NUM"
        number = 0
        try:
            number = w2n.word_to_num(word)
        except:
            number = 0

        if number != 0:
            c_type = "NUM"

        posWord = (word, c_type)
        # print(word + ":" + c_type)
        splitPosSentence.append(posWord)
        splitSentence.append(word)
        # print(',{word:"' + word["displayForm"] + '", type:"' + c_type + '"}')

    splitPosSentences.append(splitPosSentence)
    splitSentences.append(splitSentence)

print(splitPosSentences)
print()
print(splitSentences)

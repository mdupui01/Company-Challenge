import csv
import glob
import os
import re
from collections import Counter
from collections import OrderedDict

class Error( Exception ): pass

############################################################################
# First thing to do is open the text (be sure to change the filepath!)
############################################################################

filepath = "/Users/luminoso/brown_corpus/"
savePathRoot = "/Users/luminoso/"

if filepath == "/Users/luminoso/brown_corpus/":
    raise Error("Filepath needs to be changed.")
if filepath == "/Users/luminoso/":
    raise Error("Filepath for output files needs to be changed.")
if filepath[-1:] != "/":
    filepath = filepath + "/"

os.chdir(filepath)
text = []
for files in glob.glob("*c*"):
    filepathTemp =  filepath + files
    with open (filepathTemp, "r") as myfile:
        textTemp = myfile.read().replace('\n', '')
        textTemp = textTemp.split()
        text = text + textTemp



############################################################################
# Remove punctuation and organize words by plural and singular
############################################################################

def removePunctuation(segment):
    if "./." in segment:
        segment = segment.replace("./.","")
    elif ",/," in segment:
        segment = segment.replace(",/,","")
    elif ":/:" in segment:
        segment = segment.replace(":/:","")
    elif "(/(" in segment:
        segment = segment.replace("(/(","")
    elif ")/)" in segment:
        segment = segment.replace(")/)","")
    elif "``/``" in segment:
        segment = segment.replace("``/``","")
    elif "``/``" in segment:
        segment = segment.replace("''/''","")
    elif "?/." in segment:
        segment = segment.replace("?/.","")
    elif "!/." in segment:
        segment = segment.replace("!/.","")
    elif ";/." in segment:
        segment = segment.replace(";/.","")
    else:
        segment = segment
        
    if "/" not in segment:
        segment = ""
        
    if segment.count("/") >= 2: # This is to remove all remaining odd punctuation
        segment = ""

    return segment

text = [removePunctuation(segment) for segment in text]
text = filter(None,text)

def catagorize(data):
    container = [[],[],[]]
    for segment in data:
        searchWord(segment, container)
        
    return container

def searchWord(segment, container):
    word, tag = segment.split('/')
    if tag == 'nns':
        container[0].append(word)
    elif tag == 'dts':
        container[0].append(word)
    elif tag == 'ppls':
        container[0].append(word)
    elif tag == 'nn':
        container[1].append(word)
    elif tag == 'dt':
        container[1].append(word)
    elif tag == 'ppl':
        container[1].append(word)
    elif tag == 'pp$':
        container[1].append(word)
    elif tag == 'pp$$': # This tag loads both singulars and plurals. This is taken care of in the singularClean() function
        container[1].append(word)
    else:
        container[2].append(word)

list_plural, list_singular, list_other = catagorize(text)



############################################################################
# Convert plural words to singular to optimize matching
############################################################################

# The following two functions use a number of rules that I came up with.
# The basis of these rules and assumptions are described in the PDF

# Some of the tags load plural and singular pronouns and determiners
def singularClean(word): 
    word = word.lower()
    if re.match("^[A-Za-z_-]*$", word):
        if word.endswith("'s"):
            word = word[:-2]
            singular = word
        elif word.endswith("."):
            word = word[:-1]
            singular = word
        elif word.startswith("$"):
            word = "dollar"
            singular = word
        elif word == "her":
            word = "him"
            singular = word
        elif word == "hers":
            word = "his"
            singular = word
        elif word == "herself":
            word = "himself"
            singular = word
        elif word == "ours":
            list_plural.append(word)
            singular = ""
        elif word == "our":
            list_plural.append(word)
            singular = ""
        elif word == "their":
            list_plural.append(word)
            singular = ""
        elif word == "theirs":
            list_plural.append(word)
            singular = ""
        elif word == "these":
            list_plural.append(word)
            singular = ""
        else:
            singular = word
    else:
        singular = ""
        
    return singular


# It should also be noted that certain words like "mayor-nominate" should be taken into consideration. This is a singular noun, but is composed of two words. However, a mayor-nominate is not the same as a mayor...

filteredWordsSingulars = [singularClean(word) for word in list_singular]

# The following if statements in the singular() function are the rules applied for
# converting from plural to singular. Rules can easily be changed or added. The only
# thing to watch it for is words ending in "s", for which the rule has to appear 
# under the "if word.endswith("s") statement".
def singular(word):
    word = word.lower()
    if re.match("^[A-Za-z_-]*$", word):
        if word.endswith("s"):
            if word.endswith("ies"):
                word = (word[:-3] + "y")
                singularForm = word
            elif word.endswith("hes"):
                word = (word[:-3] + "h")
                singularForm = word
            elif word.endswith("xes"):
                word = (word[:-3] + "x")
                singularForm = word
            elif word.endswith("men's"):
                word = (word[:-5] + "man")
                singularForm = word
            elif word.endswith("oes"):
                word = (word[:-3] + "o")
                singularForm = word
            elif word == "ours":
                word = "mine"
                singularForm = word
            elif word == "ourselves":
                word = "myself"
                singularForm = word
            elif word == "themselves":
                word = "himself"
                singularForm = word
            elif word == "yourselves":
                word = "yourself"
                singularForm = word
            elif word == "theirs":
                word = "his"
                singularForm = word
            elif word.endswith("sses"):
                word = word[:-2]
                singularForm = word
            else:
                word = word[:-1]
                singularForm = word
        if "degree" in word:
            word = ("degree")
            singularForm = word
        if word.endswith("s'"):
            word = (word[:-2])
            singularForm = word
        if word.endswith("men"):
            word = (word[:-3] + "man")
            singularForm = word
        if word.startswith("$"):
            word = "dollar"
            singularForm = word
        if word.endswith("'s"):
            word = (word[:-2])
            singularForm = word
        if word == "these":
            word = "this"
            singularForm = word
        if word == "those":
            word = "that"
            singularForm = word
        if word == "our":
            word = "my"
            singularForm = word
        if word == "them":
            word = "him"
            singularForm = word
        if word == "their":
            word = "his"
            singularForm = word
        else:
            singularForm = word
    else:
        singularForm = ""
    
    return singularForm

#filteredWordsPlurals = filteredWords1 + filteredWords2 + filteredWords3 + filteredWords4 + filteredWords5 + filteredWords6 + filteredWords7 + filteredWords8 + filteredWords9 + filteredWords10

filteredWordsPlurals = [singular(word) for word in list_plural]

plurals = Counter(filteredWordsPlurals)
singulars = Counter(filteredWordsSingulars)
labelsPlurals, valuesPlurals = zip(*plurals.items())
labelsSingulars, valuesSingulars = zip(*singulars.items())

# Now that we have all the words "cleaned up", we have to use the counter again in case new words match

finalList = []
indexSingulars = []
indexPlurals = []
numSingulars = []
numPlurals = []
for x in labelsSingulars:
    if x in labelsPlurals:
        finalList.append(x)
        indexSingulars = labelsSingulars.index(x)
        indexPlurals = labelsPlurals.index(x)
        numSingulars.append(valuesSingulars[indexSingulars])
        numPlurals.append(valuesPlurals[indexPlurals])

noSingularList = [] 
noSingularIndex = []
noSingularValues = []
temp = []
for x in labelsPlurals:
    if x not in labelsSingulars:
        noSingularList.append(x)
        indexNoSingular = labelsPlurals.index(x)
        temp = valuesPlurals[indexNoSingular]
        noSingularValues.append(temp)

sortedList = []
DataFrame = []
percent = []
words = []
numPluralsFilter = []

for x in xrange(len(numSingulars)):
    if numSingulars[x] < numPlurals[x]:
        temp = float(numPlurals[x])/(float(numPlurals[x])+float(numSingulars[x]))*100
        temp = "%.2f" % temp
        percent.append(temp)
        words.append(finalList[x])
        numPluralsFilter.append(numPlurals[x])


############################################################################
# We now have each word, with the number of times it appears in its plural
# form and how many times as a percentage of total appearances
############################################################################

sortedPercent = [i[1] for i in sorted(zip(percent,percent), reverse = True)]
sortedWords = [i[1] for i in sorted(zip(percent,words), reverse = True)]
sortedNumbers = [i[1] for i in sorted(zip(percent,numPluralsFilter), reverse = True)]

# Displaying the ten words that appear the most frequently in their plural form
if len(sortedWords) < 10:
    X = len(sortedWords)
else:
    X = 10

for x in xrange(X):
    data1 = zip(sortedWords,sortedPercent,sortedNumbers)
    print ("%s appears %s%% of the time in its plural form" % (sortedWords[x],sortedPercent[x]))




############################################################################
# Simply creating two output files
############################################################################

ordered_fieldnames = OrderedDict([('Word',None),('Percent of plural form',None),('Number of plural forms',None)])
savepath = savePathRoot + "output_plural_and_singular.csv"
with open(savepath,'wb') as fp:
    a = csv.writer(fp,delimiter = ",")
    dw = csv.DictWriter(fp, delimiter=',', fieldnames=ordered_fieldnames)
    dw.writeheader()
    a.writerows(data1)

data2 = zip(noSingularList,noSingularValues)
    
ordered_fieldnames = OrderedDict([('Word',None),('Number of plural forms',None)])
savepath = savePathRoot + "output_only_plural.csv"
with open(savepath,'wb') as fp:
    a = csv.writer(fp,delimiter = ",")
    dw = csv.DictWriter(fp, delimiter=',', fieldnames=ordered_fieldnames)
    dw.writeheader()
    a.writerows(data2)

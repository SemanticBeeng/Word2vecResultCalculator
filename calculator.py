import csv

#Word2VecResultFile = 'Word2VecResult[LR].csv'
#Word2VecResultFile = 'Word2VecResult[LL].csv'
Word2VecResultFile = 'Word2VecResult[G].csv'

kValues = [20, 50, 100, 200, 500]
gsWords = []
word2VecResult = []
averagePrecision = 0.0
averageRecall = 0.0
LEMMA_GS_WORD_COUNT = 0

def seek(word, wordList):
    indexValue = len(wordList)
    try:
        indexValue = wordList.index(word) + 1
    except:
        pass
    return indexValue

def calError(gsWords, resltWords, n):
    xSum = 0

    for i in range(LEMMA_GS_WORD_COUNT):
        x = 0
        if ( seek(gsWords[i], resltWords) < LEMMA_GS_WORD_COUNT ):
            x = n;
        else:
            x = ( float(n)/(n-LEMMA_GS_WORD_COUNT) ) * (n - seek(gsWords[i], resltWords))

        xSum += x;

    return 1.0 - ( float(xSum)/(n * LEMMA_GS_WORD_COUNT) );


def calculate(suggestWords, gs_words, kVal):

    suggestWords = suggestWords[0:kVal]
    correctAnswers = 0
    G = len(gs_words)

    #print "Model Suggest Words: ", suggestWords
    #print "Golden Standard Words: ", gs_words

    for word in gs_words:
        if(word in suggestWords):
            #print word,
            correctAnswers += 1

    precision = 1.0 - calError(gs_words, suggestWords, kVal)
    recall = float(correctAnswers)/G

    '''print "\nmaxIndex", maxIndex
    print "correctAnswers", correctAnswers
    print "den", den
    print "G", G
    print "precision", precision
    print "recall", recall'''

    global averagePrecision
    averagePrecision += precision

    global averageRecall
    averageRecall += recall


with open('lemmatizedGoldenStandard.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        gsWords.append(row[1:])

with open(Word2VecResultFile, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        word2VecResult.append(row)

LEMMA_GS_WORD_COUNT = len(gsWords[0])
resultTable = ""

for kVal in kValues:
    for x in range(len(word2VecResult)):
        calculate([w.split(':')[0] for w in word2VecResult[x]], gsWords[x], kVal)

    global averagePrecision
    global averageRecall

    averagePrecision = averagePrecision/len(word2VecResult)
    averageRecall = averageRecall/len(word2VecResult)

    #print "Average Precision: ",  "{:1.2f}".format( averagePrecision/len(word2VecResult) )
    #print "Average Recall: ", "{:1.2f}".format( averageRecall/len(word2VecResult) )

    F1 = 0.0
    if ((averagePrecision+averageRecall) != 0):
        F1 = (2*averagePrecision*averageRecall)/(averagePrecision+averageRecall)

    resultTable += "{:1.2f}".format(averagePrecision) + ' & ' + "{:1.2f}".format(averageRecall) + ' & ' + "{:1.2f}".format(F1) + ' & '

    averagePrecision = 0
    averageRecall = 0

print resultTable[:-3]

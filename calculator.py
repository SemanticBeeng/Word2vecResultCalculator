import csv

#Word2VecResultFile = 'Word2VecResult[LR].csv'
#Word2VecResultFile = 'Word2VecResult[LL].csv'
Word2VecResultFile = 'Word2VecResult[G].csv'

kValues = [5, 10, 20, 50, 100]
gsWords = []
word2VecResult = []
averagePrecision = 0.0
averageRecall = 0.0

def calculate(suggestWords, gs_words, R):

    suggestWords = suggestWords[0:R]
    correctAnswers = 0
    G = len(gs_words)

    #print "Model Suggest Words: ", suggestWords
    #print "Golden Standard Words: ", gs_words

    maxIndex=0
    
    for word in gs_words:
        if(word in suggestWords):
            #print word,
            correctAnswers += 1
            if ( maxIndex < suggestWords.index(word) ):
                maxIndex = suggestWords.index(word)
                
    maxIndex += 1
    den = 1
    if(correctAnswers<G):
        den = R
    else:
        den = maxIndex
    
    precision = float(correctAnswers)/den
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

for kVal in kValues:
    for x in range(len(word2VecResult)):
        calculate([w.split(':')[0] for w in word2VecResult[x]], gsWords[x], kVal)

    global averagePrecision
    global averageRecall

    averagePrecision = averagePrecision/len(word2VecResult)
    averageRecall = averageRecall/len(word2VecResult)
    
    #print "Average Precision: ",  "{:1.2f}".format( averagePrecision/len(word2VecResult) ) 
    #print "Average Recall: ", "{:1.2f}".format( averageRecall/len(word2VecResult) )

    print "{:1.2f}".format( averagePrecision ), '&', "{:1.2f}".format( averageRecall ), '&', "{:1.2f}".format( (2*averagePrecision*averageRecall)/(averagePrecision+averageRecall) ), '&', 

    averagePrecision = 0
    averageRecall = 0

import csv

Word2VecResultFile = 'Word2VecResult_New.csv'
gsWords = []
word2VecResult = []
word2VecWordsOnly = []
word2VecDistanceOnly = []
word2VecFinal = []

with open('lemmatizedGoldenStandard.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        gsWords.append(row[1:])

with open(Word2VecResultFile, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        word2VecResult.append(row)


for x in range(len(word2VecResult)):
        word2VecWordsOnly.append([w.split(':')[0] for w in word2VecResult[x]])
        word2VecDistanceOnly.append([w.split(':')[1] for w in word2VecResult[x]])

row = len(word2VecResult)
for x in range(row):
    tem = []
    for a in range(200):
        tem.append(word2VecWordsOnly[x][a] + ':' + word2VecDistanceOnly[x][a])
    word2VecFinal.append(tem)

for b in range(row):
    othersWords = []
    nextIndex = 233
    for word in gsWords[b]:
        if(word not in word2VecWordsOnly[b][0:200]):
            if(word in word2VecWordsOnly[b][200:]):
                index = word2VecWordsOnly[b].index(word)
                othersWords.append(word+':'+word2VecDistanceOnly[b][index])
            else:
                othersWords.append(word+':'+word2VecDistanceOnly[b][nextIndex])
                nextIndex += 1

    word2VecFinal[b] = word2VecFinal[b] + othersWords

fileWrite = open('Word2VecResult_Max_210[LL].csv','w')
for i in range(row):
    if(i!=(row-1)):
        fileWrite.write(','.join(word2VecFinal[i]) + '\n')
    else:
        fileWrite.write(','.join(word2VecFinal[i]))
fileWrite.close()

print "Done :) "

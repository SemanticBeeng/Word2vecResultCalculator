import csv

gsTerms = []
with open('lemmatizedGoldenStandard.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        gsTerms.append(row[0])

gsTerms.append("EXIT,")

file = open('Terms.txt','w') 
file.write(",".join(gsTerms))
file.close() 

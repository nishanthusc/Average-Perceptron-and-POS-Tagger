import sys,json

modelFileName = sys.argv[1]
model = open(modelFileName,"r")
modelDict= json.load(model)
avgPer = modelDict['averagePrcp']
#wordsInVocab = modelDict['wordMap']
classList=modelDict['categoryList']
#print(classList)
passC=0
sumList=[]
totalSentence=""
for line in sys.stdin:
    sumList[:]=[]
    #print(line)
    #totalSentence=""    
    #line = "TEST "+line
    if(len(line.strip())>0):
        words = line.split()
        for m in range(0,len(classList)):
            sumline=0             
            for wor in range(0,len(words)):
                if words[wor] in avgPer[m]:
                    sumline+=avgPer[m][words[wor]]
            sumList.append(sumline)
        maxValue = max(sumList)
        predict = classList[sumList.index(maxValue)]
        
        rawWord = words[0].split(":")
        predictedTagWord = rawWord[1]+"/"+predict
        #print(predictedTagWord)
        totalSentence= totalSentence+" "+predictedTagWord
print(totalSentence.strip())
    

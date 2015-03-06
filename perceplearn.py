import sys,json,random
import copy

categoryWeights=[]
averageWeights=[]
#vectorSum = []
categoryList=[]
vectorSumList=[]
trainingFile = sys.argv[1]
modelFile = sys.argv[2]
maxErrorrate = -sys.maxsize
maxErrorCount=0
###### Getting the filenames from stdin########################

temp = list(sys.argv)
devFileName = ""
trainFileName = ""
modalFileName = ""
devIndex = ""

if "-h" in temp :
    devIndex = temp.index("-h") + 1

    if(devIndex == 2):    #perceplearn -h devfile trainfile modelfile
        devFileName = temp[2]
        trainFileName = temp[3]
        modelFileName = temp[4]
    elif(devIndex == 3):   #percpeplearn trainfile -h devfile modelfile
        devFileName = temp[3]
        trainFileName = temp[1]
        modelFileName = temp[4]
    else:                    #percpeplearn trainfile modelfile -h devfile
        devFileName = temp[4]
        trainFileName = temp[1]
        modelFileName = temp[2]

else :
    trainFileName = temp[1]
    modelFileName = temp[2]

print(trainFileName)
print(modelFileName)
print(devFileName)
def percepClassify():
    
    testFile = open(devFileName,"r")    
    linesInTest = testFile.read()
    lines = linesInTest.split("\n")
    totalCount =0
    passC=0
    sumList=[]
    sumline=0
    predict=""
    #print(len(lines))

    for line in lines:
       
        sumList[:]=[]
        if(len(line.strip())>0):
            words = line.split()
            for m in range(0,len(categoryList)):
                sumline=0             
                for wor in range(1,len(words)):
                    if words[wor] in averageWeights[m]:
                        sumline+=averageWeights[m][words[wor]]
                sumList.append(sumline)
            maxValue = max(sumList)
            predict = categoryList[sumList.index(maxValue)]
            if(predict == words[0]):
                passC+=1
            totalCount+=1
    testFile.close()
    return (passC/totalCount)
        



fileopen = open(trainFileName,'r')
fopen = fileopen.read()
lines = fopen.split("\n")
print(len(lines))
for line in lines:
    if(len(line.strip())>0):
        words = line.split()
        category = words[0]
        if category!="":
            if category not in categoryList:
                categoryList.append(category)

print(len(categoryList))

for i in range(0,len(categoryList)):
    categoryWeights.append({})
    averageWeights.append({})
    for line in lines:
        if(len(line.strip())>0):
            words = line.split()
            for j in range(1,len(words)):
                categoryWeights[i][words[j]]=0
                averageWeights[i][words[j]]=0
print("After Intialization")
#print(categoryWeights)
#print(averageWeights)

itr=0
iterations = 20
#print(lines)
while(itr<iterations):
    random.shuffle(lines)
    totalCount=0
    passCount=0
    for line in lines:
        vectorSum=0        
        
        #print(line)
        if(len(line.strip())>0):
            #print("inside")
            words = line.split()
            correctCategory = words[0]
            for k in range(0,len(categoryList)):
                for i in range(1,len(words)):
                    vectorSum+= categoryWeights[k][words[i]]
                vectorSumList.append(vectorSum)
                vectorSum=0               
                
            maxValue = max(vectorSumList)           
            predictedCategory = categoryList[vectorSumList.index(maxValue)]
            vectorSumList[:]=[]
            #print(predictedCategory,correctCategory)
            
            if(predictedCategory!=correctCategory):
                
                correctCategoryIndex = categoryList.index(correctCategory)
                predictedCategoryIndex = categoryList.index(predictedCategory)
                
                for z in range(1,len(words)):
                    categoryWeights[predictedCategoryIndex][words[z]]-=1
                    categoryWeights[correctCategoryIndex][words[z]]+=1
            else:
                passCount+=1
            totalCount+=1
    itr+=1
    print(passCount/totalCount)
    for zz in range(0,len(categoryList)):
        for wor in categoryWeights[zz]:
            averageWeights[zz][wor]+=categoryWeights[zz][wor]
    finalavgDict=averageWeights[:]
            
    if(len(devFileName) != 0):
        accuracy = percepClassify()
        if(accuracy > maxErrorrate) :
            maxErrorrate = accuracy
            maxErrorCount = 0
            finalavgDict=averageWeights[:]

        else :
            maxErrorCount+=1
        if(maxErrorCount == 5):
            print("breaking the loop after ",maxErrorCount,"iterations with accuracy",maxErrorrate)
            break
        print("accuracy on dev data",accuracy)

    #print(errorrate/total)

    errorrate = 0
    total = 0


finalDict={'averagePrcp':finalavgDict,'categoryList':categoryList}
fwrite = open(modelFileName,'w')
json.dump(finalDict,fwrite)
fwrite.close()
print("done")
##print(categoryWeights)
##print(averageWeights)          
    
            
                
        

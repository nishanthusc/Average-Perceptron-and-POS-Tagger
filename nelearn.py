import sys,os,codecs,tempfile


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

#print(trainFileName)
#print(modelFileName)
#print(devFileName)

def formatFile(line):
    totalSentence=""
    if(len(line.strip())>0):
        #print(line)
        words = line.split()
        for i in range(0,len(words)):
            if(len(words[i].strip())>0):
                sep = words[i].split("/")
                nerTag = sep[-1]
                remainingWord = "/".join(sep[:-1])
                if(len(words)==1 and i==0):
                    previousWord="prev:start"
                    nextWord="next:end"
                    out.write(nerTag+" "+"p:"+remainingWord+" "+previousWord+" "+nextWord)
                elif(i==0):
                    previousWord="prev:start"
                    nerTag = sep[-1]
                    currentWord = remainingWord
                    nextWordArr = words[i+1].split("/")
                    nextword = "/".join(nextWordArr[:-1])
                    out.write(nerTag+" "+"p:"+currentWord+" "+previousWord+" "+"next:"+nextword+"\n")
                elif(i==len(words)-1):
                    nextWord="next:end"
                    currentWord = remainingWord
                    previousWordArr = words[i-1].split("/")
                    previousWord = "/".join(previousWordArr[:-1])
                    out.write(nerTag+" "+"p:"+currentWord+" "+"prev:"+previousWord+" "+nextWord+"\n")
                elif(i!=0 and i<len(words)-1):
                    currentWord = remainingWord
                    prevWordArr = words[i-1].split("/")
                    previousWord = "/".join(prevWordArr[:-1])
                    nextWordArr = words[i+1].split("/")
                    nextWord = "/".join(nextWordArr[:-1])
                    out.write(nerTag+" "+"p:"+currentWord+" "+"prev:"+previousWord+" "+"next:"+nextWord+"\n")
                else:
                    pass
                #totalSentence+=stng
    #print(totalSentence)

tempHolder = tempfile.NamedTemporaryFile(delete = False)
out = open(tempHolder.name,"w")
fread = open(trainFileName,"r",errors='ignore')
lines  =fread.read().split("\n")

for line in lines:
    formatFile(line)

traingTemFname = tempHolder.name

if(len(devFileName.strip())>0):
    devRead = open(devFileName,"r",errors='ignore')
    devOut = tempfile.NamedTemporaryFile(delete = False)
    out = open(devOut.name,"w")
    dRead = devRead.read().split("\n")
    for line in dRead:
        formatFile(line)
    devFname = devOut.name
    devOut.close()
#print(devFname)
#print(traingTemFname)
os.system("python3 ../perceplearn.py "+traingTemFname+" "+modelFileName+" -h "+devFname)

#print("done")



        
    
                
            
            

import sys,os
import tempfile

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



count=0
temp = 0
def formatout(line,tempFname):
    global count,temp
    if(len(line) == 0):
        return
    line = line.replace("/"," ")
    words = line.split()
    if (len(words) < 3):
        out.write(words[1]+" p:"+words[0]+" prev:start next:end\n")
        temp = temp + 1
        count = count + 1
        return
    out.write(words[1]+" "+"p:"+words[0]+" prev:start"+" "+"next:"+words[2]+"\n")
    count = count + 1
    index = 2;
    while(index < len(words)):
        if index == len(words) - 2 :
            break
        out.write(words[index+1]+" "+"p:"+words[index]+" "+"prev:"+words[index-2]+" "+"next:"+words[index+2]+"\n")
        count = count + 1
        index =index + 2
    out.write(words[index+1]+" "+"p:"+words[index]+" "+"prev:"+words[index-2]+" "+"next:end"+"\n")
    count = count + 1

tempHolder = tempfile.NamedTemporaryFile(delete = False)

out = open(tempHolder.name,"w")
fread = open(trainFileName,"r")
lines = fread.read().split("\n")

for line in lines :
    formatout(line,out)
traingTemFname = tempHolder.name
#out.close()
#print(traingTemFname)
if(len(devFileName.strip())>0):
    devRead = open(devFileName,"r",errors='ignore')
    devOut = tempfile.NamedTemporaryFile(delete = False)
    out = open(devOut.name,"w")
    dRead = devRead.read().split("\n")
    for line in dRead:
        formatout(line,devOut)
    devFname = devOut.name
    devOut.close()

#print(count)
#print(temp)
#print(devFname)
#print(traingTemFname)
#print("done formatting")
#print("calling perceptron learn")
#fname = out.name
os.system("python3 ../perceplearn.py "+traingTemFname+" "+modelFileName+" -h "+devFname)

print("done")



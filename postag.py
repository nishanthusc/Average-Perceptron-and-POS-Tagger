import sys,codecs,subprocess

modelFile = sys.argv[1]
sys.stdin = codecs.getreader('utf8')(sys.stdin.detach(), errors='ignore')

for line in sys.stdin:
    if(len(line.strip())>0):
        lineStr=""
        words = line.split()
        for i in range(0,len(words)):
            if(len(words)==1):
                stng = "p:"+words[i]+" "+"prev:start"+" "+"next:end"+"\n"
            elif(i==0):
    ##            mainword = words[0].split("/")
    ##            tagWord = mainword[1]
    ##            feature = mainword[0]
    ##            nextfeature = words[i+1].split("/")
                stng = "p:"+words[i]+" "+"prev:start"+" "+"next:"+words[i+1]+"\n"
            elif(i==len(words)-1):
    ##            mainword = words[i].split("/")
    ##            tagWord = mainword[1]
    ##            feature = mainword[0]
    ##            prevfeature = words[i-1].split("/")            
                stng = "p:"+words[i]+" "+"prev:"+words[i-1]+" "+"next:end"+"\n"
            elif(i!=0 and i<len(words)):
    ##            mainword = words[i].split("/")
    ##            prevWord = words[i-1].split("/")
    ##            nextWord = words[i+1].split("/")
                stng = "p:"+words[i]+" "+"prev:"+words[i-1]+" "+"next:"+words[i+1]+"\n"
            else:
                pass
            lineStr+=stng
        #print(lineStr)
        proc = subprocess.Popen(['python3','percepclassify.py',modelFile],  stdin=subprocess.PIPE)
        proc.stdin.write(lineStr.encode())
        proc.communicate()[0]
        proc.wait()
            

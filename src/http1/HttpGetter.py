'''
Created on Jun 13, 2014

@author: michael_bal
'''


class HttpGetter(object):
    
    def __init__(self):
        
        from http import client
        self.connection = client.HTTPConnection("metacyc.org")
        print(self.connection.host)
        
    def getResult(self,idlist,file):
        import re
        begginRequestStr = "/HUMAN/substring-search?type=COMPOUND&object="
        endRequestStr = "&quickSearch=Quick+Search"

        #print( res.status) 
        #print( res.reason) 
        #print(data1)
        for id1 in reversed(idlist):
            id1 = re.sub("\([0-9]-\)","",id1)
            self.connection.request("GET", begginRequestStr+ id1.replace(" ","+").replace(",","+") +endRequestStr, None, {})
            res = self.connection.getresponse()
            data1 = res.read()
            if res.reason == 'OK' and "No matches found " not in str(data1):
                print('match')
                return 0
        

        
        if len(idlist)>0:
            print(idlist[0] + '\n')
            file.write(idlist[0] + '\n')
        file.close()
        return 1



    def createReconMets(self,fileName):
        ins = open( fileName, "r" )
        reconMets = []
        for line in ins:
            values = line.split("\t")
            if len(values)<2:
                print(values)
            else:
                ids =[]
                name = values[1].replace("\n","")
                if name != "":
                    ids.append(name)
                if len(values)>=6:
                    name = values[5].replace("\n","")
                    if name != "":
                        ids.append(name)
                reconMets.append(ids)        
        ins.close()
        return reconMets


httpGetter = HttpGetter()
counter = 0


reconMets  = httpGetter.createReconMets('names.tsv')
for ids in reconMets:
    outFile = open('missingMets2.txt',"a")
    counter = counter +  httpGetter.getResult(ids,outFile)
    print(str(counter) +'\n')   
print(counter)   
    
    
    
    
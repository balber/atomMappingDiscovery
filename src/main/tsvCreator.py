'''
Created on May 27, 2014

@author: michael_bal
'''
from main.Reaction import Reaction

class tsvCreator(object):

    def __init__(self,compundSet):
        self.compundSet = compundSet
        
    def createTsvFile(self,fileName,reactions):
        file = open(fileName,"w+t")
        file.write(Reaction.getTsvColumnsNames())
        for reaction in reactions:
            file.write(reaction.getAsTabSeperatedLine()+'\n')
            
    def createMetsTsv(self,NameToMetRecon):
        file = open('metabolites.tsv',"w+t")
        file.write('recon name\t' + 'has match in metaCyc\t' + 'ids\n')
        c=0
        
        for met in NameToMetRecon.values():
            
            if met.metaCycMetList != []:
                names=[]
                for met in met.metaCycMetList:
                    names.append(met.name)
                names = '  ;  '.join(names)
                file.write( met.name + '\t' + 'True\t' +' '.join(met.ids)+ '\t' + names + '\t'+met.formula+'\n')
                c=c+1
            else:
                file.write( met.name+ '\t' + 'False\t' +' '.join(met.ids)+ '\n')
        print('compounds')
        print(c)
        file.close()
        



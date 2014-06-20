'''
Created on May 6, 2014

@author: michael_bal
'''
from main.Metabolite import Metabolite
from main.Reaction import Reaction

RESOURCE_PATH_PREFIX = "..\\resources\\"


class DataParser(object):

    def createReconMetsMap(self,fileName):
        ins = open( fileName, "r" )
        reconNameToMetMap = {}
        for line in ins:
            met = Metabolite(line)
            reconNameToMetMap[met.name] = met
        ins.close()
        print(len(reconNameToMetMap.keys()))
        
        ins = open(    RESOURCE_PATH_PREFIX + 'reconMetsFormulas.tsv')
        for line in ins:
            values = line.split('\t')
            if values[0] in reconNameToMetMap.keys():
                reconNameToMetMap[values[0]].setFormulaFromString(values[1])
            else:
                print(values[0])
        ins.close()
        
        return reconNameToMetMap
        
    
    def nameToIdsMetaCycCreate(self,fileName):
        import itertools as it
        myMap = {}
        with open(fileName,'r') as f:
            for key,group in it.groupby(f,lambda line: line.startswith('//')):
                if not key:
                    name=''
                    met  = Metabolite()
                    for line in group:
                        if 'UNIQUE-ID' in line:
                            name = line.split(' - ')[1]
                            met.name = name.replace("\n",'')                       
                            met.ids.append(met.name)
                        elif 'DBLINKS' in line:
                            str1 = line.split(' - ')
                            id1 = str1[1].split('"')[1]
                            met.ids.append(id1)
                                              
                        elif 'CHEMICAL-FORMULA' in line:
                            str1 = line.split(' - ')
                            if str1[1] != '':   #example str1[1] = (C 12)
                                str1 = str1[1].split("(")[1].split(")")[0] #str1 = C 12  
                                strs = str1.split(" ")
                                met.formulaMap[strs[0]] = strs[1]
                                
                    if(met.ids != [] and met.name != ''):
                        myMap[met.name] = met
                        
        return myMap
    
    def extractAllReactions(self,fileName,NameToMetMeta,compoundSet):
        import itertools as it
        fullReactions = []
        partialReactions = []
        counter=0
        with open(fileName,'r') as f:
            for key,group in it.groupby(f,lambda line: line.startswith('//')):
                if not key:
                    counter=counter+1
                    reaction = Reaction(group,NameToMetMeta,compoundSet)
                    
                    if(reaction.left == [] or None in reaction.left or 
                        reaction.right == [] or None in reaction.right ):
                        partialReactions.append(reaction)
                    else:
                        fullReactions.append(reaction)
                                      
        print('meta reactions: ')
        print(counter)                        
        return fullReactions, partialReactions

    
    def matchReactions(self,reconReactions , metaCycReactions):
        counter = 0
        
        for recon in reconReactions:
            for meta in metaCycReactions:
                if (self.cpmReactionList(recon.left,meta.left) and self.cpmReactionList(recon.right,meta.right)) or (self.cpmReactionList(recon.left,meta.right) and self.cpmReactionList(recon.right,meta.left)):
                #if compareReactionsLeftToRight(recon , meta) or cmpReactionsRightToLeft(recon,meta):
                    recon.atomMapping = meta.atomMapping
                    recon.hasMatch=True
                    if  meta.atomMapping != [] :   
                        counter = counter +1
                    break
        print(counter)        
    
    
    def cpmReactionList(self,reconList , metaList):
        for met1 in reconList:
            isOk = False
            if met1.metaCycMetList == []:
                return False
            for met2 in metaList:
                if met1.isMyName(met2.name):
                    isOk=True
                    break
                    
            if(not isOk):
                return False    
        
        return True
    
     
    def setCompoundsMetaCycCreate(self,fileName):
    #from sets import Set
        set1 = set()
        with open(fileName,'r') as f:
            for line in f:
                if 'DBLINKS' in line:
                    str1 = line.split(' - ')
                    id1 = str1[1].split('"')[1]
                    set1.add(id1.lower())
                
        return set1 
     
    def matchAllMets(self,NameToMetRecon, NameToMetMeta):
        for reconMet in NameToMetRecon.values():
            for metaCycMet in NameToMetMeta.values():
                if reconMet.equals(metaCycMet):
                    reconMet.metaCycMetList.append(metaCycMet)
    
      
    
   
       
#     def matchPartial(self,reconPartial, metaCycReactions):
#         counter = 0
#         for recon in reconPartial:
#             for meta in metaCycReactions:
#                 if self.comparePartialReactionsLeftToRight(recon , meta) or self.cmpPartialReactionsRightToLeft(recon,meta):
#                     recon.atomMapping = meta.atomMapping
#                     if  meta.atomMapping != [] :   
#                         counter = counter +1
#                     break
#         print(counter)        
    
                            

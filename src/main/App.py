'''
Created on May 6, 2014

@author: michael_bal
'''
from main.Reaction import Reaction
from main.Metabolite import Metabolite
from main.tsvCreator import tsvCreator

def createReconMetsMap(fileName):
    ins = open( fileName, "r" )
    reconNameToMetMap = {}
    for line in ins:
        met = Metabolite(line)
        reconNameToMetMap[met.name] = met
    ins.close()
    print(len(reconNameToMetMap.keys()))
    
    ins = open('reconMetsFormulas.tsv')
    for line in ins:
        values = line.split('\t')
        if values[0] in reconNameToMetMap.keys():
            reconNameToMetMap[values[0]].setFormulaFromString(values[1])
        else:
            print(values[0])
    ins.close()
    
    return reconNameToMetMap
    


def extractAllReactions(fileName,NameToMetMeta,compoundSet):
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

def nameToIdsMetaCycCreate(fileName):
    import itertools as it
    map = {}
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
                        if met.name == 'CPD-8574':
                            r=1
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
                    map[met.name] = met
                    
    return map

#creates


                    
def nameToIdsReconCreate(fileName):
    import itertools as it
    map = {}
    with open(fileName,'r') as f:
        for key,group in it.groupby(f,lambda line: line.startswith('//')):
            if not key:
                for line in group:
                    if 'LEFT' in line or 'RIGHT' in line:
                        ids = line.split(' - ')[1]
                        ids = ids.split('\t')
                        idsFix = []
                        for id1 in ids:
                            idsFix.append(id1.replace("\n",''))                               
                        map[idsFix[0]] = idsFix                           
    return map    


def comparePartialReactionsLeftToRight(recon, meta):
    pass
        


def cmpPartialReactionsRightToLeft(recon, meta):
    pass


def matchPartial(reconPartial, metaCycReactions):
    counter = 0
    for recon in reconReactions:
        for meta in metaCycReactions:
            if comparePartialReactionsLeftToRight(recon , meta) or cmpPartialReactionsRightToLeft(recon,meta):
                recon.atomMapping = meta.atomMapping
                if  meta.atomMapping != [] :   
                    counter = counter +1
                break
    print(counter)        

    

def matchReactions(reconReactions , metaCycReactions):
    counter = 0
    
    for recon in reconReactions:
        for meta in metaCycReactions:
            if (cpmReactionList(recon.left,meta.left) and cpmReactionList(recon.right,meta.right)) or (cpmReactionList(recon.left,meta.right) and cpmReactionList(recon.right,meta.left)):
            #if compareReactionsLeftToRight(recon , meta) or cmpReactionsRightToLeft(recon,meta):
                recon.atomMapping = meta.atomMapping
                recon.hasMatch=True
                if  meta.atomMapping != [] :   
                    counter = counter +1
                break
    print(counter)        


def cpmReactionList(reconList , metaList):
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

def totalMapCreate():
    NameToMetRecon = nameToIdsReconCreate('recon2ReactionsNotEmpty.txt')
    NameToIdsReconFromName = createReconMetsMap('names.tsv')
    
    for key in NameToMetRecon.keys():
        if NameToMetRecon[key] != NameToIdsReconFromName[key]:
            r=1
 
 
 
def setCompoundsMetaCycCreate(fileName):
#from sets import Set
    set1 = set()
    with open(fileName,'r') as f:
        for line in f:
            if 'DBLINKS' in line:
                str1 = line.split(' - ')
                id1 = str1[1].split('"')[1]
                set1.add(id1.lower())
            
    return set1 
 
def matchAllMets(NameToMetRecon, NameToMetMeta):
    for reconMet in NameToMetRecon.values():
        for metaCycMet in NameToMetMeta.values():
            if reconMet.equals(metaCycMet):
                reconMet.metaCycMetList.append(metaCycMet)

      
#NameToKeggMetaCyc = nameToIdMetaCycCreate('compounds.dat') #11227 compounds
compoundSet = setCompoundsMetaCycCreate('compounds.dat')

tsvcreator = tsvCreator(compoundSet)

NameToMetMeta = nameToIdsMetaCycCreate('compounds.dat')

NameToMetRecon = createReconMetsMap('names.tsv')

matchAllMets(NameToMetRecon,NameToMetMeta)
tsvcreator.createMetsTsv(NameToMetRecon)


reconReactions, reconPartial = extractAllReactions('recon2ReactionsByNameFiltered.txt',NameToMetRecon,compoundSet)
print(len(reconReactions))
metaCycReactions , p = extractAllReactions('reactions.dat',NameToMetMeta,compoundSet)
print(len(metaCycReactions))

#matchPartial(reconPartial , metaCycReactions)

matchReactions(reconReactions , metaCycReactions)
tsvcreator.createTsvFile('reactions.tsv',reconReactions)

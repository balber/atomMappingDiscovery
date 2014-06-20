'''
Created on Jun 20, 2014

@author: michael_bal
'''
from main.DataParser import DataParser, RESOURCE_PATH_PREFIX
from main.tsvCreator import tsvCreator
from main.Comperator import Comperator


if __name__ == '__main__':
    
    
    parser = DataParser()
    comperator = Comperator()
    compoundSet = parser.setCompoundsMetaCycCreate(RESOURCE_PATH_PREFIX + 'compounds.dat')
    
    tsvcreator = tsvCreator(compoundSet)
    
    NameToMetMeta = parser.nameToIdsMetaCycCreate(RESOURCE_PATH_PREFIX +'compounds.dat')
    
    NameToMetRecon = parser.createReconMetsMap(RESOURCE_PATH_PREFIX+'names.tsv')
    
    comperator.matchAllMets(NameToMetRecon,NameToMetMeta)
    tsvcreator.createMetsTsv(NameToMetRecon)
    
    
    reconReactions, reconPartial = parser.extractAllReactions(RESOURCE_PATH_PREFIX +'recon2ReactionsByNameFiltered.txt',NameToMetRecon,compoundSet)
    print(len(reconReactions))
    metaCycReactions , p = parser.extractAllReactions(RESOURCE_PATH_PREFIX + 'reactions.dat',NameToMetMeta,compoundSet)
    print(len(metaCycReactions))
    
    #matchPartial(reconPartial , metaCycReactions)
    
    comperator.matchReactions(reconReactions , metaCycReactions)
    tsvcreator.createTsvFile(RESOURCE_PATH_PREFIX+'reactions.tsv',reconReactions)
    
    
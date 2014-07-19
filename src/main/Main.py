'''
Created on Jun 20, 2014

@author: michael_bal
'''
from main.DataParser import DataParser, RESOURCE_PATH_PREFIX
from main.OutputFileCreator import OutputFileCreator
from main.Comperator import Comperator
#import pdb

if __name__ == '__main__':    
    
    parser = DataParser()
    comperator = Comperator()
        
    NameToMetMeta = parser.nameToIdsMetaCycCreate(RESOURCE_PATH_PREFIX +'compounds.dat')
    NameToMetRecon = parser.createReconMetsMap(RESOURCE_PATH_PREFIX+'names.tsv')
    
    comperator.matchAllMets(NameToMetRecon,NameToMetMeta)
   
    reconReactions, reconPartial = parser.extractAllReactions(RESOURCE_PATH_PREFIX +'recon2ReactionsByNameFiltered.txt',NameToMetRecon)
    print(len(reconReactions))
    
    metaCycReactions , p = parser.extractAllReactions(RESOURCE_PATH_PREFIX + 'reactions.dat',NameToMetMeta)
    print(len(metaCycReactions))
    
    #matchPartial(reconPartial , metaCycReactions)    
    comperator.matchReactions(reconReactions , metaCycReactions)
    
    outputFileCreator = OutputFileCreator()
    outputFileCreator.createMetsTsv(NameToMetRecon)
    outputFileCreator.createTsvFile(RESOURCE_PATH_PREFIX+'reactions.tsv',reconReactions)  
    outputFileCreator.createTotalHtmlFile(NameToMetRecon, reconReactions)
    
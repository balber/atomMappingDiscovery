'''
Created on Jun 20, 2014

@author: michael_bal
'''
from main.DataParser import DataParser, RESOURCE_PATH_PREFIX
from main.tsvCreator import tsvCreator
from main.Comperator import Comperator
from main.html import HTML

if __name__ == '__main__':
    
    
    parser = DataParser()
    comperator = Comperator()
    compoundSet = parser.setCompoundsMetaCycCreate(RESOURCE_PATH_PREFIX + 'compounds.dat')
    
    tsvcreator = tsvCreator(compoundSet)
    
    NameToMetMeta = parser.nameToIdsMetaCycCreate(RESOURCE_PATH_PREFIX +'compounds.dat')
    
    NameToMetRecon = parser.createReconMetsMap(RESOURCE_PATH_PREFIX+'names.tsv')
    
#     htmString = tsvcreator.listToHtml(NameToMetRecon.values(),'metabolites:')
#     file = open('mets.htm','w+t')
#     file.write(str(htmString))
#     file.close()
#     print('finish html')
    comperator.matchAllMets(NameToMetRecon,NameToMetMeta)
    tsvcreator.createMetsTsv(NameToMetRecon)
    
    
    reconReactions, reconPartial = parser.extractAllReactions(RESOURCE_PATH_PREFIX +'recon2ReactionsByNameFiltered.txt',NameToMetRecon,compoundSet)
    print(len(reconReactions))
    
    metaCycReactions , p = parser.extractAllReactions(RESOURCE_PATH_PREFIX + 'reactions.dat',NameToMetMeta,compoundSet)
    print(len(metaCycReactions))
    
    #matchPartial(reconPartial , metaCycReactions)
    
    comperator.matchReactions(reconReactions , metaCycReactions)
    tsvcreator.createTsvFile(RESOURCE_PATH_PREFIX+'reactions.tsv',reconReactions)
    
#     htmString = tsvcreator.listToHtml(reconReactions,'reactions:')
#     file = open('reacs.htm','w+t')
#     file.write(str(htmString))
#     file.close()
#     print('finish reactions html')
    
    
    h=HTML('html')
    #h += HTML('body','hi')
    bod = h.body
    div1 = bod.div
    div1.h1('Metabolites:')
    for met in NameToMetRecon.values():
        div1 += met.toHtml()
    
    div2 = bod.div
    div2.h1('Reactions:')
    for reac in reconReactions:
        div2 += reac.toHtml() 
    
    file = open('all data.htm','w+t')
    file.write(str(h))
    file.close()
    print('finish reactions html')
    
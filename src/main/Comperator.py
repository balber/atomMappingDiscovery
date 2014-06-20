'''
Created on Jun 20, 2014

@author: michael_bal
'''

class Comperator(object):
    
    def matchAllMets(self,NameToMetRecon, NameToMetMeta):
        for reconMet in NameToMetRecon.values():
            formulaEqualeSet = set()
            idEqualset = set()
            for metaCycMet in NameToMetMeta.values(): 
                if reconMet.cmpFormula(metaCycMet):
                    formulaEqualeSet.add(metaCycMet)
                if reconMet.cmpIds(metaCycMet):
                    idEqualset.add(metaCycMet)
            
            intersectionSet = idEqualset & formulaEqualeSet
            if len(intersectionSet) != 0:
                reconMet.metaCycMetSet =  intersectionSet 
            else:
                if len(idEqualset) == 0:
                    reconMet.metaCycMetSet = formulaEqualeSet
                else:
                    reconMet.metaCycMetSet = idEqualset
            
    def cpmReactionList(self,reconList , metaList):
        for met1 in reconList:
            isOk = False
            if len(met1.metaCycMetSet)==0:
                return False
            for met2 in metaList:
                if met1.isMyName(met2.name):
                    isOk=True
                    break
                    
            if(not isOk):
                return False    
        
        return True

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
    
                            
        
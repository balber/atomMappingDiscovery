'''
Created on Jun 20, 2014

@author: michael_bal
'''
import pdb
class Comperator(object):
    
    def matchAllMets(self,NameToMetRecon, NameToMetMeta):
        reconMets = NameToMetRecon.values()
        count=0
        formulaCounter=0
        a=0
        for reconMet in reconMets:
#             if reconMet.name == "L-citrulline" :
#                     a=1
#                     pdb.set_trace()
            formulaEqualeSet = set()
            idEqualset = set()
            keggEualSet = set()
            for metaCycMet in NameToMetMeta.values():
                
                if reconMet.cmpFormula(metaCycMet):
                    formulaEqualeSet.add(metaCycMet)
#                     if a==1:
#                         pdb.set_trace()
                if reconMet.cmpIds(metaCycMet):
                    idEqualset.add(metaCycMet)
                    
                if reconMet.cpmKegg(metaCycMet):
                    keggEualSet.add(metaCycMet)
#                     if a==1:
#                         pdb.set_trace()
#                         b=2
#             intersectionSet = idEqualset & formulaEqualeSet
#             if len(intersectionSet) != 0:
#                 reconMet.metaCycMetSet =  intersectionSet 
#             else:
#                 if len(formulaEqualeSet) != 0:
#                     reconMet.metaCycMetSet = formulaEqualeSet
#                 else:
#                     reconMet.metaCycMetSet = idEqualset
            
            
#             if len(formulaEqualeSet)==0:
#                 reconMet.metaCycMetSet = idEqualset
#                 if(len(idEqualset)!=0):
#                     formulaCounter +=1
#             else:
#                 reconMet.metaCycMetSet = formulaEqualeSet
            if  len(keggEualSet)  != 0:
                reconMet.metaCycMetSet = keggEualSet
            else:
                if len(idEqualset) == 0:
                    reconMet.metaCycMetSet = formulaEqualeSet
                    if(len(formulaEqualeSet)!=0):
                        formulaCounter +=1
                else:
                    reconMet.metaCycMetSet = idEqualset
                
                
            if len(reconMet.metaCycMetSet)!=0:
                count += 1
        print('number of matched reactions is : ' + str(count) )
        print('formulaCounter = ' + str(formulaCounter)) 
            
            
    def cpmReactionList(self,reconList , metaList):
        if len(reconList)!=len(metaList):
            return False
        
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
                    recon.metaCycReaction = meta
                    counter = counter +1
                    #if  meta.atomMapping != [] :   
                        
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
    
                            
        
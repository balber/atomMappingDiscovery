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
        for reconMet in reconMets:
#             if reconMet.name == "L-citrulline" :
#                     a=1
#                     #pdb.set_trace()
            formulaEqualeSet = set()
            idEqualset = set()
            keggEqualSet = set()
            for metaCycMet in NameToMetMeta.values():
                
                if reconMet.cmpFormula(metaCycMet):
                    formulaEqualeSet.add(metaCycMet)
#                     if a==1:
#                         #pdb.set_trace()
                if reconMet.cmpIds(metaCycMet):
                    idEqualset.add(metaCycMet)
                    
                if reconMet.cpmKegg(metaCycMet):
                    keggEqualSet.add(metaCycMet)
#                     if a==1:
#                         #pdb.set_trace()
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
            if  len(keggEqualSet)  != 0:
                reconMet.metaCycMetSet = keggEqualSet
            else:
                if len(idEqualset) != 0:
                    reconMet.metaCycMetSet = idEqualset
                else:                    
                    reconMet.metaCycMetSet = formulaEqualeSet
                    if(len(formulaEqualeSet)!=0):
                        formulaCounter +=1
                
                
            if len(reconMet.metaCycMetSet)!=0:
                count += 1
        print('number of matched reactions is : ' + str(count) )
        print('formulaCounter = ' + str(formulaCounter)) 
            
            
    def cpmReactionList(self,reconList , metaList):
        #pdb.set_trace()
        if len(reconList)!=len(metaList):
            #pdb.set_trace()
            return False
        
        for met1 in reconList:
            #pdb.set_trace()
            isOk = False
            if len(met1.metaCycMetSet)==0:
                #pdb.set_trace()
                return False
            #pdb.set_trace()
            for met2 in metaList:
                #pdb.set_trace()
                if met1.isMyName(met2.name):
                    #pdb.set_trace()
                    isOk=True
                    break
                #pdb.set_trace()
            if(not isOk):
                #pdb.set_trace()
                return False    
        #pdb.set_trace()
        return True

    def matchReactions(self,reconReactions , metaCycReactions):
        counter = 0
        
        for recon in reconReactions:
#            if recon.name != 'CYSAMOe':
#               continue
            #pdb.set_trace()
            for meta in metaCycReactions:
                #if meta.uniqueId!='CYSTEAMINE-DIOXYGENASE-RXN':
                #    continue
                #pdb.set_trace()
                leftDirection = (self.cpmReactionList(recon.left,meta.left) and self.cpmReactionList(recon.right,meta.right))
                #pdb.set_trace()
                rightDirection = (self.cpmReactionList(recon.left,meta.right) and self.cpmReactionList(recon.right,meta.left))
                #pdb.set_trace()
                if leftDirection  or rightDirection:
                #if compareReactionsLeftToRight(recon , meta) or cmpReactionsRightToLeft(recon,meta):
                    #pdb.set_trace()
                    recon.atomMapping = meta.atomMapping
                    recon.hasMatch=True
                    recon.metaCycReaction = meta
                    counter = counter +1
                    #if  meta.atomMapping != [] :   
                        
                    break
            #pdb.set_trace()
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
    
                            
def printCollection(col):
    for element in col:
        print(element.name)        
'''
Created on May 27, 2014

@author: michael_bal
'''
from main.Reaction import Reaction
from main.DataParser import RESOURCE_PATH_PREFIX
from main.html import HTML


class OutputFileCreator(object):

        
    def createTsvFile(self,fileName,reactions):
        file = open(fileName,"w+t")
        file.write(Reaction.getTsvColumnsNames())
        for reaction in reactions:
            file.write(reaction.getAsTabSeperatedLine()+'\n')
            
    def createMetsTsv(self,NameToMetRecon):
        file = open(RESOURCE_PATH_PREFIX + 'metabolites.tsv',"w+t")
        file.write('recon name\t' + 'has match in metaCyc\t' + 'ids\t' + 'number of reactions included' +'\n')
        for met in NameToMetRecon.values():
            
            if len(met.metaCycMetSet) != 0:
                names=[]
                for met1 in met.metaCycMetSet:
                    names.append(met1.name)
                names = '  ;  '.join(names)
                file.write( met.name + '\t' + 'True\t' +' '.join(met.ids)+ '\t' + str(len(met.reactionList)) + '\t' + names + '\t'+met.formula.replace("\n","")+'\n')
            else:
                file.write( met.name+ '\t' + 'False\t' +' '.join(met.ids)+ '\t' + str(len(met.reactionList)) + '\n')

        file.close()

        
    def createTotalHtmlFile(self,NameToMetRecon, reconReactions):
        h = HTML('html')
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
        
        file = open(RESOURCE_PATH_PREFIX + 'all data.htm', 'w+t')
        file.write(str(h))
        file.close()
        print('finish reactions html')
        
        
        
        
        
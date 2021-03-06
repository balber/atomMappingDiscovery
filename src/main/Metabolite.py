'''
Created on Jun 16, 2014

@author: michael_bal
'''
from main.html import HTML
import re
import pdb
METACYC_COMPOUND_PREFIX='http://metacyc.org/META/NEW-IMAGE?type=COMPOUND&object='
KEGG_PREFIX='http://www.genome.jp/dbget-bin/www_bget?cpd:'
class Metabolite(object):

    def __init__(self, line=''):
        self.name=""
        self.metaCycMetSet=set()
        self.ids=[]
        self.keggId = ""
        self.hasKeggIdMatch = False
        self.reactionList=[]
        self.formula=""
        self.formulaMap = {}
        if line != '':
            values = line.split("\t")
            self.name = values[0].replace("\n","")
            #self.ids.append(self.name)
            for id1 in values[1:]:
                if id1 != "" and id1 != "\n":
                    if "\n" in id1:
                        id1 = id1.replace("\n","")
                    self.ids.append(id1)
                    if re.match("[cC][0-9]+", id1):
                        self.keggId = id1.lower()


    def setFormulaFromString(self, formulaStr):
        import re
        molecules = re.findall("[A-Z][a-z]*[0-9]*", formulaStr)
        for molecule in molecules:
            number = re.split("[A-Z][a-z]*",molecule)[1]
            name = molecule.replace(number,"")
            name = name.upper()
            if number == '':
                number="1"
            self.formulaMap[name] = number
            self.formula+=name
            self.formula+=number



    def cmpFormula(self, met):
        if len(self.formulaMap.keys()) == 0:
            return False
        
        if len(self.formulaMap.keys()) != len(met.formulaMap.keys()):
            return False
        
        for molecule in self.formulaMap.keys():
            if molecule not in met.formulaMap.keys() or self.formulaMap[molecule] != met.formulaMap[molecule]:
                return False
    
        return True
    
    def cpmKegg(self,met):
        if self.keggId == met.keggId and met.keggId!="":
            self.hasKeggIdMatch = True
            return True   
        return False
    
    def cmpIds(self, met):         
        
        for id1 in self.ids:
            for id2 in met.ids:
                if id1.lower() == id2.lower():
                    return True
        return False
            
        
    def equals(self, met):
        
        return self.cmpFormula(met) or self.cmpIds(met)
        
    def isMyName(self,name):
        #pdb.set_trace()        
        for met in self.metaCycMetSet:
            #pdb.set_trace()
            if met.name == name:
                #pdb.set_trace()
                return True
        #pdb.set_trace()
        return False
        
    def toHtml(self):
        h = HTML()
        l=h.li
        l.h3.a('Metabolite recon name: ' + self.name, id=self.name)
        l.p('has MetaCyc match: ' + str(len(self.metaCycMetSet)!=0))
        l.p('formula: ' + self.formula)
        
        hasKegg = False
        idsStr=''
        for id1 in self.ids:
            idsStr+=id1
            idsStr+='    ;    '
            if id1.startswith('C'):
                hasKegg=True
                keggId=id1
        l.p('ids: ' + idsStr)
        if hasKegg:
            l.p.a('kegg link' , href=KEGG_PREFIX+keggId)
#         metaCycNames=''
#         for met in self.metaCycMetSet:
#             metaCycNames+=met.name
#             metaCycNames+='    ;    '
#         l.p('metaCyc posible matches: ' + metaCycNames)
#         
        par = l.ul('metaCyc posible matches: ',newlines=True)
        for met in self.metaCycMetSet:
            par.li.a(met.name + '  ;  ' , href=METACYC_COMPOUND_PREFIX+met.name)

        par = l.ul('recon reactions: ',newlines=True)
        for reac in self.reactionList:
            par.li.a(reac.toLine()+'\n' , href='#'+reac.name)
        return h


met = Metabolite()
met.toHtml()            
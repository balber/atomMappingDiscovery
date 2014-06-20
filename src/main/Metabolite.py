'''
Created on Jun 16, 2014

@author: michael_bal
'''

class Metabolite(object):

    def __init__(self, line=''):
        self.name=""
        self.metaCycMetList=[]
        self.ids=[]
        self.reactionList=[]
        self.formula=""
        self.formulaMap = {}
        if line != '':
            values = line.split("\t")
            self.name = values[0].replace("\n","")
            self.ids.append(self.name)
            for id1 in values[1:]:
                if id1 != "" and id1 != "\n":
                    if "\n" in id1:
                        id1 = id1.replace("\n","")
                    self.ids.append(id1)


    def setFormulaFromString(self, formulaStr):
        import re
        self.formula=formulaStr
        molecules = re.findall("[A-Z][a-z]*[0-9]*", formulaStr)
        for molecule in molecules:
            number = re.split("[A-Z][a-z]*",molecule)[1]
            name = molecule.replace(number,"")
            if number == '':
                number="1"
            self.formulaMap[name] = number


    def cmpFormula(self, met):
        if len(self.formulaMap.keys()) != len(met.formulaMap.keys()):
            return False
        
        for molecule in self.formulaMap.keys():
            if molecule not in met.formulaMap.keys() or self.formulaMap[molecule] != met.formulaMap[molecule]:
                return False
    
        return True
    
    
    def cmpIds(self, met):
        for id1 in self.ids:
            for id2 in met.ids:
                if id1.lower() == id2.lower():
                    return True
        return False
            
    
    
    def equals(self, met):
        
        return self.cmpFormula(met) or self.cmpIds(met)
        
    def isMyName(self,name):
        for met in self.metaCycMetList:
            if met.name == name:
                return True
        return False
        
        
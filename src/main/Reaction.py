'''
Created on May 12, 2014

@author: michael_bal
'''
from main.html import HTML
METACYC_REACTION_LINK_PREFIX = 'http://metacyc.org/META/new-image?type=REACTION&object='
class Reaction:

    def __init__(self,group,nameToMetMap):
        self.atomMapping = []
        self.name=''
        self.ecn = ''
        self.hasMatch=False
        self.metaCycReaction=None
        self.left=[]
        self.right=[]
        self.missingMets=[]
        self.nameToIdMap = nameToMetMap
        self.options = {'UNIQUE-ID' : self.uniqueIdExtract,
           'ATOM-MAPPINGS' : self.atomMappingExtract,
           'LEFT' : self.leftExtract,
           'RIGHT' : self.rightExtract,
           'RXN_NAME' : self.nameExtract,
           'EC-NUMBER' : self.ecnExtract,
           'REACTION-DIRECTION' : self.directionExtract}
        
        for line in group:
            line = line.split('\n')[0]
            strs = line.split(' - ')
            if strs[0] in self.options.keys():
                self.options[strs[0]](strs[1])          
         
        self.nameToIdMap ={}    #we only used it for construction but we dont want to save it

    def uniqueIdExtract(self,endLine):
        self.uniqueId = endLine
   
    def atomMappingExtract(self,endLine):
        if 'NO-HYDROGEN-ENCODING' in endLine: 
            self.atomMapping.append(endLine)
        
    def leftExtract(self,endLine):
        name = endLine.split('\t')[0]
        name = name.replace('|','')
        if(name not in self.nameToIdMap.keys()):
            self.left.append(None)
            return
        
        #idList = self.nameToIdMap[name].ids
        self.left.append(self.nameToIdMap[name])
        self.nameToIdMap[name].reactionList.append(self)
        
    def rightExtract(self,endLine):
        name = endLine.split('\t')[0]
        name = name.replace('|','')
        if(name not in self.nameToIdMap.keys()):
            self.right.append(None)
            return
        
        #idList = self.nameToIdMap[name].ids
        self.right.append(self.nameToIdMap[name])
        self.nameToIdMap[name].reactionList.append(self)

    
    def directionExtract(self,endLine):
        self.direction = endLine
        
    def nameExtract(self,endLine):
        self.name = endLine
        
    def ecnExtract(self,endLine):
        endLine = endLine.replace("EC-","")
        self.ecn = endLine
        
    def getAsTabSeperatedLine(self):
        leftNames=[]
        missingNames=""
        for met in self.left:
            leftNames.append(met.name)
            if len(met.metaCycMetSet)==0:
                missingNames += met.name
                missingNames += '    ;   '
        leftNames = '+'.join(leftNames)
        rightNames=[]
        for met in self.right:
            rightNames.append(met.name)
            if len(met.metaCycMetSet)==0:
                missingNames += met.name
                missingNames += '    ;   '
        rightNames = '+'.join(rightNames)
        
        return '\t'.join([self.name ,self.ecn ,str(self.hasMatch),str(self.atomMapping!=[]),leftNames,rightNames,missingNames])
    
    @staticmethod
    def getTsvColumnsNames():
        return '\t'.join(['reaction name' , 'ECN','has match in metaCyc','contains atom mapping','left mets','right mets','missingMets'])+'\n'
    
    def toHtml(self):
        h = HTML()
        l=h.li
        l.h3.a('Reaction recon name: ' + self.name, id=self.name)
        l.p('has atom mapping: ' + str(self.atomMapping!=[]))
        l.p('ecn: ' + self.ecn)
        
        if self.hasMatch==False:
            l.p.font('has metaCyc match: ' +  str(self.hasMatch),color="red")
        else:
            l.p.font('has metaCyc match: ' +  str(self.hasMatch),color="blue")
        if self.metaCycReaction != None:
            l.p.a('metaCyc reaction name: ' + self.metaCycReaction.uniqueId , href=METACYC_REACTION_LINK_PREFIX+ self.metaCycReaction.uniqueId)
        else:
            l.p('metaCyc reaction name: ')
        par = l.p( 'left:' ,newlines=False)
        for met in self.left:
            if len(met.metaCycMetSet)==0:
                par.a(href='#'+met.name).font(met.name + '  +  ',color="red")
            else:
                par.a(met.name + '  +  ' , href='#'+met.name)
         
        par = l.p( 'right:' ,newlines=False)
        for met in self.right:
            if len(met.metaCycMetSet)==0:
                par.a(href='#'+met.name).font(met.name + '  +  ',color="red")
            else:
                par.a(met.name + '  +  ' , href='#'+met.name)#         txt = ''
        return h
   

    def toLine(self):
        txt=''
        for met in self.left:
            if met == None:
                txt += '_____'
            else:
                txt += met.name
            txt += ' + '
        txt = txt[:-3]
        txt+= ' -> '
        for met in self.right:
            if met == None:
                txt += '_____'
            else:
                txt += met.name
            txt += ' + '
        txt = txt[:-3]
        
        return txt  
'''
Created on May 12, 2014

@author: michael_bal
'''
class Reaction:

    def __init__(self,group,nameToMetMap,compundSet):
        self.atomMapping = []
        self.name=''
        self.ecn = ''
        self.hasMatch=False
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
                
            #if 'reactionRunningCounter' in line:
            #   self.recNum = line.split(':')[1]
       # for idlist in self.left:
        #    mySet = set()
         #   for s in idlist:
          #      mySet.add(s.lower())
           # if len(idlist)>0 and len( compundSet & mySet)==0:
            #    self.missingMets.append(idlist[0])
            
         
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
            print(name)
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
        for met in self.left:
            met = met.ids
            if len(met)>0:
                leftNames.append(met[0])
        leftNames = '+'.join(leftNames)
        rightNames=[]
        for met in self.right:
            met=met.ids
            if len(met)>0:
                rightNames.append(met[0])
        rightNames = '+'.join(rightNames)
        missingNames=[]
        for name in self.missingMets:
            if len(name)>0:
                missingNames.append(name)
        
        missingNames = '    ;   '.join(missingNames)
        return '\t'.join([self.name ,self.ecn ,str(self.hasMatch),str(self.atomMapping!=[]),leftNames,rightNames,missingNames])
    
    @staticmethod
    def getTsvColumnsNames():
        return '\t'.join(['reaction name' , 'ECN','has match in metaCyc','contains atom mapping','left mets','right mets','missingMets'])+'\n'
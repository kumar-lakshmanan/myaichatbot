'''
@name: 
@author: kayma
@createdon: "2026-03-26"
@description:
'''

__created__ = "2026-03-26"
__updated__ = "2026-03-26"
__author__  = "kayma"

import os,sys
import kTools

class Conversation():
    
    def __init__(self):
        self.tls = kTools.KTools() 
        
        self.save_conversation = 1
        self.conversation_file_path = ".conversation\coding"
        
        self._extAllowed = ['.01user','.02assistent','.03tools']
                  
        
    def initialize(self):
        #Initialize system
        #Is conversation folder exists or not
        if self.save_conversation:
            if not self.tls.isFolderExists(self.conversation_file_path):
                self.tls.debug(f"Create conversation folder [{self.conversation_file_path}]")
                self.tls.pathReady(self.conversation_file_path)
    
    def _saveConversation(self, convType, content):
        '''
        convType = 01user or 02assistent or 03tools
        '''
        timeStamp = self.tls.getDateTimeStamp()
        fileName = f"{timeStamp}.{convType}"        
        convFile = self.tls.pathJoin(self.conversation_file_path, fileName)
        if self.save_conversation:
            self.tls.debug(f"Saving conversation to file {convFile}")        
            self.tls.writeFileContent(convFile, content)
        return convFile
    
    def saveUserMsg(self, content):
        return self._saveConversation('01user', content)
    
    def saveAIMsg(self, content):
        return self._saveConversation('02assistent', content)    
    
    def saveToolsMsg(self, content):
        return self._saveConversation('03tools', content)    
    
    def _getConversations(self):
        fullConv = ""
        cnt = 0        
        if self.tls.isFolderExists(self.conversation_file_path):
            self.tls.debug(f"Reading conversation folder [{self.conversation_file_path}]")
            convFiles = self.tls.getFileList(self.conversation_file_path, extAllowed = self._extAllowed)
            for eachConvFile in convFiles:
                self.tls.debug(f"Reading file [{eachConvFile}]")    
                eachConvFile = eachConvFile.lower()
                if eachConvFile.endswith(tuple(self._extAllowed)):
                    fPath, fName, fExt = self.tls.pathParts(eachConvFile)
                    convType = fExt.replace(".","").replace("01","").replace("02","").replace("03","").upper()
                    convContent = self.tls.getFileContent(eachConvFile)
                    fullConv += f"{convType}:\n{convContent}\n"
                    cnt += 1
            self.tls.debug(f"No.of files read: [{cnt}]")
        
        allConv = ''
        if cnt > 0 and len(fullConv) > 1:
            allConv = "These are our earlier conversation, Use these for reference and answer my recent query!\n\n"
            allConv + fullConv
        return allConv   

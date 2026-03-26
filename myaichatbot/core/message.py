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

class Messages():
    
    def __init__(self):
        self.tls = kTools.KTools() 
        
        self._messages = []
        
        self.filterLastMsgDuplicate = 1
        self.filterFileContentDuplicate = 1
    
    def _showVerbose(self, txt: str = "Added msg"):
        self.tls.debug(f'Added Msg: {txt[:300]} ...',3)
            
    def _msg_structure(self, msg: str, role: str = "user") -> dict:
        dct = {"role": role, "content": msg}
        return dct

    def getLastMsgToolName(self):
        if len(self._messages):
            return self._messages[-1]['tool_name']
        else:
            return ''
    
    def getLastMsgType(self):
        if len(self._messages):
            return self._messages[-1]['role']
        else:
            return ''
        
    def addMessage(self, msg: str,  role: str = "user"):
        dictMsg = self._msg_structure(msg, role)
           
        allMessage = self.getAllMessages()
        lastMessage = allMessage[-1] if len(allMessage) else self._msg_structure(None)
        
        if self.filterFileContentDuplicate:
            if not (lastMessage['role'] == role and lastMessage['content'] == msg):
                return dictMsg
            else:
                self._showVerbose("Not adding duplicate message!")
        return None
    
    def addUserMessage(self,  msg: str):
        msg = self.addMessage(msg, "user")
        if msg: self._messages.append(msg)
        if msg: self._showVerbose(str(msg))

    def addSystemMessage(self,  msg: str):
        msg = self.addMessage(msg, "system")
        if msg: self._messages.append(msg)
        if msg: self._showVerbose(str(msg))        

    def addAssistantMessage(self,  msg: str):
        msg = self.addMessage(msg, "assistant")
        if msg: self._messages.append(msg)                
        if msg: self._showVerbose(str(msg))

    def addToolMessage(self,  msg: str, toolName: str):
        msg = self.addMessage(msg, "tool")
        if msg: msg['tool_name'] = toolName
        if msg: self._messages.append(msg)    
        if msg: self._showVerbose(str(msg))

    def isMessageAvailable(self) -> []:
        return len(self._messages) 
        
    def getAllMessages(self) -> []:
        return self._messages
    
    def clearMessages(self):
        self._messages = []      
    
    def addReferenceFileContent(self, fileContents: str, forceUpdate: bool = False):
        header = "Here are the file content for your references, Use them to answer the queries if it really needed.\n"
        updatedMsg = header + fileContents
        
        if self.filterFileContentDuplicate:
            allMessage = self.getAllMessages()
            alreadyAdded = False
            for eachMsg in allMessage:
                if eachMsg['role'] == 'user' and header in eachMsg['content']:
                    alreadyAdded = True
                    break
                
            if not alreadyAdded:
                self.addUserMessage(updatedMsg)
            else:
                if forceUpdate:
                    allMessage = self.getAllMessages()
                    for index, eachMsg in enumerate(allMessage):
                        if eachMsg['role'] == 'user' and header in eachMsg['content']:
                            msgDict = self._messages.pop(index)
                            msgDict['content'] = updatedMsg 
                else:
                    self._showVerbose("File contents already added.")
        else:
            self.addUserMessage(updatedMsg)
        
          
        
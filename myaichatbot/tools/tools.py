'''
@name: 
@author: kayma
@createdon: "2026-03-26"
@description:
'''

__created__ = "2026-03-26"
__updated__ = "2026-03-26"
__author__  = "kayma"

import os, sys
import kTools
from .custom_tools import web_action

class Tools():
    
    def __init__(self):
        self.tls = kTools.KTools() 
        self._tools = {}

    def addCustomTools(self):
        # File/Folder operation
        self.addTool(self.tls.getFileContent)
        self.addTool(self.tls.writeFileContent)
        self.addTool(self.tls.cleanFolder)
        self.addTool(self.tls.copyFolder)
        self.addTool(self.tls.makePath)
        self.addTool(self.tls.forceDeleteFile)
        self.addTool(self.tls.isFileExists)
        self.addTool(self.tls.isItFile)
        self.addTool(self.tls.isItFolder)
        
        # Ollama based web actions
        self.addTool(web_action.webSearch)
        self.addTool(web_action.webFetch)
    
    def _fetchToolFn(self, toolName):
        return self._tools[toolName] if toolName in self._tools else None
    
    def excecuteTool(self, toolName, toolArgs):
        response = None
        fn = self._fetchToolFn(toolName)
        if fn:
            try:
                self.tls.info(f"AI Invoking tool: [{toolName}] with arg [{str(toolArgs)[:100]}]")
                response = fn(**toolArgs)
            except:
                err = self.tls.getLastErrorInfo()
                self.tls.error(err)
        else:
            self.tls.error(f"Tool not found [{toolName}]")
        return response

    def getToolsFn(self):
        return self._tools.values()     

    def getToolsNames(self):
        return self._tools.keys()
        
    def addTool(self, fn):
        name = fn.__name__
        self.tls.debug(f'Attaching tool [{name}]')
        alreadyAdded = False
        for eachToolName in self.getToolsNames():
            if eachToolName == name:
                alreadyAdded = True
        if not alreadyAdded:
            self._tools[name] = fn

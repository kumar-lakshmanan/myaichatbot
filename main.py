import os, sys
import ollama

from commonlib import kTools
import lookup

from lib import message
from lib import utils
from lib import tools
from lib import conversation

APP_NAME = "MyAIChatBot"
CONFIG_FILE = "config.json"
LOOKUP_FILE = lookup

class MyAIChatBot():

    def __init__(self):
        self.tls = kTools.KTools(APP_NAME, LOOKUP_FILE, CONFIG_FILE)
        self.utils = utils.Utilities()
        
        self.verbose = tls.getValue('verbose')
        self.repeatCoreCallingCountLimit = tls.getValue('repeatCoreCallingCountLimit')
        
        self.simulate = tls.getValue('simulate')
        self.save_prompt = tls.getValue('save_prompt')
        self.prompt_file = tls.getValue('prompt_file')            
        self.save_conversation = tls.getValue('save_conversation')
        self.include_past_conversation = tls.getValue('include_past_conversation')
        self.include_reference_files = tls.getValue('include_reference_files')
        
        self.ai_definition = tls.getValue('ai_definition', tls.getValue('ai_definition_for_general'))
        
        self.conversation_file_path = tls.getValue('conversation_file_path')
        self.reference_files_paths = tls.getValue('reference_files_paths')
        self.reference_files_includeonly = tls.getValue('reference_files_includeonly')
        self.reference_files_exclude = tls.getValue('reference_files_exclude')      
        
    def initialize(self):
        self.tls.info("Initializing...")
        
        self.tls.turnOnDebugLogs(self.verbose)
        
        self._prepare_ai_agent()  
        self._prepare_messages()
        self._prepare_tools()
        
        self.msg.addSystemMessage(self.ai_definition)
         
    def _prepare_tools(self):
        self.tls.info("Preparing AI tools...")
        self.tools = tools.Tools()
        self.tools.addCustomTools()
            
    def _prepare_ai_agent(self):
        self.tls.info("Preparing AI agent...")
        
        self.tls.debug("Checking OLLAMA_API_KEY...")
        _ollama_api_key = self.tls.getValue('OLLAMA_API_KEY')
        if not _ollama_api_key:
            self.tls.errorAndExit("Ollama API key not found. Please set OLLAMA_API_KEY in env to proceed")
        
        self.tls.debug("Readying Ollama Client...")
        self._client = ollama.Client()    
    
    def _prepare_messages(self):
        self.tls.info("Preparing message handler...")
        self.msg = message.Messages()
        self.msg.filterLastMsgDuplicate = 1
        self.msg.filterFileContentDuplicate = 1

    def _prepare_conversation(self):
        self.conv = conversation.Conversation()
        self.conv.conversation_file_path = self.conversation_file_path
        self.conv.save_conversation = self.save_conversation
        self.conv.initialize()
                    
        if self.include_past_conversation:            
            content = self.conv._getConversations()
            self.msg.addSystemMessage(content)  
                    
    def _prepare_reference_files(self):
        if self.include_reference_files:
            folder_paths = self.reference_files_paths
            exclude_filter = self.reference_files_exclude
            include_filter = self.reference_files_includeonly
            allRefFileContent = ""
            if len(folder_paths):
                for eachRefFolderPath in folder_paths:
                    self.tls.info(f"Reading files from {eachRefFolderPath}")
                    refFileContent = self.utils.read_files(eachRefFolderPath, exclude_filter, include_filter)
                    allRefFileContent += refFileContent
                if allRefFileContent:
                    self.msg.addReferenceFileContent(allRefFileContent)
        
    def _add_reponse(self, msg):
        self._final_reponse += "\n" + str(msg).strip()
    
    def get_response(self):
        return self._final_reponse.strip()
            
    def _save_prompt(self):
        if self.save_prompt:
            data = ''
            for eachMsg in self.msg.getAllMessages():
                role = eachMsg['role']
                content = eachMsg['content']
                data += f'\nRole: {role}\nContent: {content}\n'
            if len(data):
                self.tls.debug(f"Saving complete prompt to {self.prompt_file}")
                self.tls.writeFileContent(self.prompt_file, data)
                        
    def chat(self, qry):        
        self._internal_ai_call = 0
        self._repeatCoreCallCurrCount = 0
        self._final_reponse = ""
        
        if qry and len(qry):
            qry = qry.strip()         
            self._internal_ai_call = 0   
            self.tls.info(f"You: {qry}")
            self.msg.addUserMessage(qry)
        
        self._prepare_conversation()
        self._prepare_reference_files()
       
        if self.msg.isMessageAvailable():
            self.conv.saveUserMsg(qry)
            self._save_prompt()
            self._coreChat()
            self.conv.saveAIMsg(self.get_response())
        
    def _coreChat(self):        
        if not self.simulate:
            if self._internal_ai_call: self.tls.debug(f"Running internal call...")
            self.tls.info("Please, wait executing ai call...")        
            currResponse = self._client.chat(self.tls.getValue("mainModel"), 
                                         messages = self.msg.getAllMessages(), 
                                         tools = self.tools.getToolsFn(),
                                         stream=False, 
                                         think=False)
            
            respMsg = str(currResponse["message"]["content"]).strip()
            respDur = currResponse['total_duration'] / 1_000_000_000
            respTools = currResponse["message"].tool_calls
            
            #self.tls.info(f"Done! Received currResponse in {respDur} Sec")
            self.tls.info(f"AI: {respMsg.strip()} ...")
            
            if respMsg and self.msg.getLastMsgType() == 'user':
                self._add_reponse(respMsg)
                self.msg.addAssistantMessage(respMsg)

            if respMsg and self.msg.getLastMsgType() == 'tool':
                toolName = self.msg.getLastMsgToolName()
                self._add_reponse(respMsg)
                self.msg.addToolMessage(respMsg, toolName)
            
            if respTools and len(respTools):
                for eachTool in respTools:
                    fnName = eachTool.function.name
                    fnArgs = eachTool.function.arguments
                    toolsResp = self.tools.excecuteTool(fnName, fnArgs)
                    self._add_reponse(toolsResp)
                    self.msg.addToolMessage(toolsResp, fnName)    
                    
                    #For safty purpose, calling the AI agent again to double check. All are done. else let it action.
                    self._internal_ai_call = 1
                    self._coreChat()
            else:   
                if self._internal_ai_call == 1:
                    # No more tool execution needed. Lets stop.
                    # But will ask AI itself to confirm, all are done, and ask for a STOP signal.
                    # Before that will see, if it last response says. somethign completed or done.
                    # Also will make sure its executing only for controlled limit of reexcution. 
                    self.tls.debug("All tools executed. Lets check the resp msg and confirm if it needed ai call again.")
                    
                    if (not self.utils.is_agent_actually_done(respMsg)) and (self._repeatCoreCallCurrCount < self.repeatCoreCallingCountLimit):
                        self._repeatCoreCallCurrCount += 1 
                        msg = "Have you completed all requested tasks? If yes, please explicitly state 'All tasks completed.' If not, continue with remaining tasks."
                        self.msg.addUserMessage(msg)
                        self._coreChat()
                    else:
                        self.tls.debug("Agent completed its task or no.of attempt to work completed.")
                        return "done"
                else:
                    self.tls.debug("Agent done. No tool to execute.")
                    return "done"
                    
        else:
            self.tls.info("Simulation Done!")          

if __name__ == "__main__":
    tls = kTools.KTools(APP_NAME, LOOKUP_FILE, CONFIG_FILE)
    mcb = MyAIChatBot()
    mcb.initialize()
    qry = '''
        I have commonlib.kTools. a simple lib for supporting any python development.
        Read that file and Create a readme.md in commonlib. Listing down all features of kTools. 
    '''
    mcb.chat(qry)
    tls.info(f"You: {qry}")
    tls.info(f"AI: {mcb.get_response()}")
    tls.info("Done")
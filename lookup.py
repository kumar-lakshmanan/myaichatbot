'''
KMX Tools Configuration

#Desc:
All CONSTANTS, STRING HARD CODES. SETTINGS ARE PRESENT HERE

#Usage (Via KMXTOOLS):
self.lookUp = self.setUpLookUp(customPyLookUp)
self.lookUp.JsonConfigFile

#Also:
KMXTOOLS.GETPARAMETER

'''

import os,sys
import datetime

__app__ = 'MyAIChatBot'
__appName__ = 'My AI CHATBOT'
__desc__ = 'My AI Chat bot for supporting me with all development activity'
__creater__ = 'Kumaresan Lakshmanan'
__date__ = '2025-03-12'
__version__ = '0.0.1'
__updated__ = '2026-03-16'
__release__ = 'Test'

versionStr = "v%s" % __version__
versionInfo ='%s (%s)' % (versionStr, __updated__)
contactInfo = 'Contact kaymatrix@gmail.com for more info.'

JsonConfigFile = 'config.json'
envVarJsonConfigFile = 'KMXJSONCONFIG'  #ENV Variable to mention that JSON COnfig File

timeStampFormat = '%Y%m%d%H%M%S'
dateTimeFormat = '%Y-%m-%d %I:%M:%S %p'

logDisable = 0
logLevel = 'DEBUG'       #DEBUG, INFO, WARN, ERROR
logDateTimeFormat = '%Y-%m-%d %I:%M:%S%p'
logFormat = '[%(asctime)s] %(module)s - %(funcName)s() [%(levelname)s] %(message)s'
logFormat = '[%(asctime)s]%(levelname).1s:%(message)s'
logToConsole = 1
logToFile = 1
logFile = 'output.log'
logModuleName = 1

ciperKey = 4132     #Four digit secret key
randomSeed = 89

#AI chatbot config
mainModel = 'qwen3-coder:480b-cloud'
websearchModel = 'gpt-oss:20b-cloud'

ai_definition_for_general = f"""
You are my expert adviser with upto date world knowledge as on {datetime.date.today()}. 
for all my queries, explain me point by point or section by section or step by step. any thing simpler manner.
use web search and give latest, recent, updated messages every time when ever needed.
"""

ai_definition_for_coding = f"""
You are my helpful, friendly, AI coding assistant. with good and upto-date coding knowledge as on {datetime.date.today()}.  
Help me build, understand, refine python based applications and scripts.
"""


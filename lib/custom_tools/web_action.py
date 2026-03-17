'''
@name: 
@author: kayma
@createdon: "2026-03-26"
@description:
'''

__created__ = "2026-03-26"
__updated__ = "2026-03-26"
__author__  = "kayma"
import os
from ollama import chat, web_fetch, web_search
import datetime

from commonlib import kTools

def webSearch(qry: str) -> str:
    '''
    tool to perform - ollama based web search 
    '''    
    tls = kTools.KTools()
        
    tls.debug(f"Internal tool invoked to do web search for {qry}")
    
    available_tools = {'web_search': web_search}
    
    resp = ""
    messages = []
    messages.append({'role': 'system', 'content': f'You are a helpful AI assistant, Always does a web search as of {datetime.date.today()} to get recent latest info. and answer the users query. Let the response be short and precise, but include necessary requested details.'})
    messages.append({'role': 'user', 'content': str(qry).strip()})

    while True:
        response = chat(
          model=tls.getValue('websearchModel'),
          messages=messages,
          tools=[web_search],
          think=True
          )
        if response.message.thinking:
            tls.info(f'Web tool, internal thinking: {response.message.thinking}')
        if response.message.content:
            respMsg = str(response.message.content).strip()
            resp += respMsg.encode('utf-8', errors='ignore').decode('utf-8')
            messages.append(response.message)
        if response.message.tool_calls:
            tls.info(f'Web tool, internal calls: {response.message.tool_calls}')
            for tool_call in response.message.tool_calls:
                function_to_call = available_tools.get(tool_call.function.name)
                if function_to_call:
                    args = tool_call.function.arguments
                    #args['model'] = model
                    #args['token'] = token                   
                    result = function_to_call(**args)
                    tls.info(f'Web tool, internal result: {str(result)[:200]}...')
                    # Result is truncated for limited context lengths
                    messages.append({'role': 'tool', 'content': str(result)[:2000 * 4], 'tool_name': tool_call.function.name})
                else:
                    messages.append({'role': 'tool', 'content': f'Tool {tool_call.function.name} not found', 'tool_name': tool_call.function.name})
        else:
            break
         
    return resp

def webFetch(url: str) -> str:
    '''
    tool to perform - ollama based web fetch 
    '''    
    tls = kTools.KTools()
        
    tls.debug(f"Tool invoked to do web fetch for {url}")
    
    available_tools = {'web_fetch': web_fetch}
    
    resp = ""
    messages = []
    messages.append({'role': 'system', 'content': f'You are a helpful AI assistant, Always does a web search as of {datetime.date.today()} to get recent latest info. and answer the users query.'})
    messages.append({'role': 'user', 'content': str(url).strip()})

    while True:
        response = chat(
          model=tls.getValue('websearchModel'),
          messages=messages,
          tools=[web_fetch],
          think=True
          )
        if response.message.thinking:
            tls.info(f'Web tool, internal thinking: {response.message.thinking}')
        if response.message.content:
            respMsg = response.message.content
            resp += respMsg.encode('utf-8', errors='ignore').decode('utf-8')
            #print('Content: ', response.message.content)
        messages.append(response.message)
        if response.message.tool_calls:
            tls.info(f'Web tool, internal calls: {response.message.tool_calls}')
            for tool_call in response.message.tool_calls:
                function_to_call = available_tools.get(tool_call.function.name)
                if function_to_call:
                    args = tool_call.function.arguments
                    result = function_to_call(**args)
                    tls.info(f'Web tool, internal result: {str(result)[:200]}...')
                    # Result is truncated for limited context lengths
                    messages.append({'role': 'tool', 'content': str(result)[:2000 * 4], 'tool_name': tool_call.function.name})
                else:
                    messages.append({'role': 'tool', 'content': f'Tool {tool_call.function.name} not found', 'tool_name': tool_call.function.name})
        else:
            break
         
    return resp

import os, sys

import kTools

class Utilities():
    
    def __init__(self):
        self.tls = kTools.KTools() 
        self._tmp_cnt = 0
        
    def read_files(self, folder_path, exclude_filter=None, include_filter=None):
        """
        Recursively read a project folder and create a big string with file contents.
        
        Args:
            folder_path (str): Path to the project folder
            exclude_filter (list): List of words that should NOT be present in file path
            include_filter (list): List of words that MUST be present in file path
        
        Returns:
            str: Big string containing all filtered file contents with headers
            
        # Example 1: Read all files except those with 'test' or 'temp' in path
        result1 = read_project_folder(
            "/path/to/your/project",
            exclude_filter=['test', 'temp']
        )
        
        # Example 2: Read only files with 'src' or 'lib' in path, excluding 'backup'
        result2 = read_project_folder(
            "/path/to/your/project",
            exclude_filter=['backup'],
            include_filter=['src', 'lib']
        )
        
        # Example 3: Read all files (only using exclude filter)
        result3 = read_project_folder(
            "/path/to/your/project",
            exclude_filter=['node_modules', '.git']
        )
        
        print(result3[:500])  # Print first 500 characters            
        """
        
        # Initialize filters if None
        if exclude_filter is None:
            exclude_filter = []
        if include_filter is None:
            include_filter = []
        
        result = ""
        self._tmp_cnt = 0
        
        def should_include_file(file_path):
            """Check if file should be included based on filters"""
            # Check exclude filter - if any excluded word is in path, skip file
            for exclude_word in exclude_filter:
                if exclude_word in file_path:
                    return False
            
            # If include filter is empty, only use exclude filter
            if not include_filter:
                return True
                
            # Check include filter - if any required word is in path, include file
            for include_word in include_filter:
                if include_word in file_path:
                    return True
                    
            # If include filter exists but no required word found, skip file
            return False
        
        def read_directory(current_path):
            """Recursively read directory contents"""
            nonlocal result
            
            try:
                # Get all items in current directory
                items = os.listdir(current_path)
                
                # Sort items to maintain consistent order
                items.sort()
                
                for item in items:
                    item_path = os.path.join(current_path, item)
                    
                    # If it's a directory, recurse into it
                    if os.path.isdir(item_path):
                        read_directory(item_path)
                    # If it's a file, process it
                    elif os.path.isfile(item_path):
                        # Apply filters
                        if should_include_file(item_path):
                            try:
                                self.tls.debug(f"Including file: {item_path}")
                                self._tmp_cnt += 1
                                with open(item_path, 'r', encoding='utf-8') as file:
                                    content = file.read()
                                    # Add file header and content to result
                                    result += f"File: {item_path}\n"
                                    result += content
                                    result += "\n\n"  # Two newlines as separator
                            except (UnicodeDecodeError, PermissionError):
                                # Skip files that can't be read as text or don't have permission
                                continue
                                
            except PermissionError:
                # Skip directories we don't have permission to read
                pass
        
        # Start recursive reading from the root folder
        read_directory(folder_path)
        self.tls.info(f"No.of files read {self._tmp_cnt}")
        return result
    
    def is_agent_actually_done(self, responseMessage):
        """
        More sophisticated check for completion
        """
        responseMessage = responseMessage.strip()
        
        completedMsg = "All tasks completed."
        if responseMessage == completedMsg or completedMsg in responseMessage:
            return True
        
        # If response is very short and doesn't indicate ongoing work
        if len(responseMessage) < 50:
            non_completion_keywords = ["done", "completed", "finished", "ready", "prepared"]
            completion_keywords = ["Let me", "working on", "need to", "will", "next", "continue", "remaining"]
            
            content_lower = responseMessage.lower()
            has_completion_keyword = any(keyword in content_lower for keyword in non_completion_keywords)
            has_continuation_keyword = any(keyword in content_lower for keyword in completion_keywords)
            
            return has_completion_keyword and not has_continuation_keyword
        
        # If response mentions specific next steps
        continuation_phrases = [
            "next step", "next i will", "next we", "continuing with",
            "now i will", "now we", "proceed to", "move on to"
        ]
        
        return not any(phrase in responseMessage.lower() for phrase in continuation_phrases)    

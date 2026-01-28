# agents/code_implementation.py
from crewai import Agent
from tools.file_operations import modify_file
from tools.code_analysis_tools import read_file_system

def create_code_implementation_agent(llm):
    """Create the Code Implementation Agent"""
    
    code_implementation_agent = Agent(
        role="Skilled Development Engineer",
        goal="Execute refactoring plans by making precise, safe modifications to code files while preserving functionality",
        backstory="""You are a detail-oriented software engineer with 8 years of experience in code 
        refactoring and maintenance. You excel at implementing complex refactoring strategies with 
        surgical precision. Your reputation is built on making safe, incremental changes that improve 
        code quality without breaking existing functionality. You are methodical, always double-check 
        your work, and have an excellent track record of zero-defect refactoring implementations. 
        You understand the importance of maintaining code semantics while improving structure and readability.""",

        llm=llm,
        
        verbose=True,
        allow_delegation=False,
        tools=[
            modify_file,
            read_file_system
        ],
        
        max_iter=5,
        memory=True
    )
    
    return code_implementation_agent
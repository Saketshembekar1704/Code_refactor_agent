# agents/refactor_strategist.py
from crewai import Agent
from tools.code_analysis_tools import read_file_system

def create_refactor_strategist_agent(llm):
    """Create the Refactor Strategist Agent"""
    
    refactor_strategist_agent = Agent(
        role="Senior Software Architect & Refactoring Strategist",
        goal="Create comprehensive, step-by-step refactoring plans based on code analysis reports to improve code quality and maintainability",
        backstory="""You are a highly experienced software architect with 15+ years in the industry. 
        You specialize in large-scale code refactoring and have successfully modernized dozens of legacy 
        codebases. Your strength lies in breaking down complex refactoring tasks into manageable, 
        sequential steps that minimize risk while maximizing improvement. You understand the delicate 
        balance between code improvement and maintaining functionality. You always prioritize safety 
        and create detailed action plans that junior developers can follow confidently.""",
        
        llm=llm,

        verbose=True,
        allow_delegation=False,
        tools=[
            read_file_system
        ],
        
        max_iter=3,
        memory=True
    )
    
    return refactor_strategist_agent
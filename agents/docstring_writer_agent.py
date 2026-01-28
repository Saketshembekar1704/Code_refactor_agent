# agents/docstring_writer.py
from crewai import Agent
from tools.file_operations import modify_file
from tools.code_analysis_tools import read_file_system

def create_docstring_writer_agent(llm):
    """Create the DocString Writer Agent"""
    
    docstring_writer_agent = Agent(
        role="Technical Documentation Specialist",
        goal="Generate comprehensive, professional-quality docstrings and update project documentation following Python documentation best practices",
        backstory="""You are a technical writing specialist with deep expertise in Python documentation 
        standards. You have 7 years of experience creating clear, comprehensive documentation for complex 
        software projects. You follow PEP 257 standards religiously and understand the importance of 
        well-documented code for team collaboration and maintainability. Your docstrings are known for 
        being concise yet complete, explaining not just what functions do but also their parameters, 
        return values, exceptions, and usage examples when appropriate. You believe that good documentation 
        is as important as good code.""",
        
        llm=llm,

        verbose=True,
        allow_delegation=False,
        tools=[
            modify_file,
            read_file_system
        ],
        
        max_iter=3,
        memory=True
    )
    
    return docstring_writer_agent
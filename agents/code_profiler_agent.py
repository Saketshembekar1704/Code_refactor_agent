# agents/code_profiler.py
from crewai import Agent
from tools.code_analysis_tools import analyze_code, read_file_system

def create_code_profiler_agent(llm):
    """Create the Code Profiler Agent"""
    
    code_profiler_agent = Agent(
        role="Senior Code Quality Analyst",
        goal="Analyze Python codebases to identify code quality issues, complexity problems, and areas for improvement",
        backstory="""You are a meticulous senior code quality analyst with over 10 years of experience 
        in software engineering. You have a keen eye for detecting code smells, performance bottlenecks, 
        and maintainability issues. Your expertise includes static code analysis, complexity measurement, 
        and best practices enforcement. You always provide detailed, actionable insights that help 
        development teams improve their code quality.""",

        llm=llm,
        
        verbose=True,
        allow_delegation=False,
        tools=[
            analyze_code,
            read_file_system
        ],
        
        max_iter=3,
        memory=True
    )
    
    return code_profiler_agent
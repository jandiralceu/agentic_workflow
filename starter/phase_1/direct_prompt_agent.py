"""
Direct Prompt Agent implementation

These scripts will help verify that the DirectPromptAgent works correctly 
and give you a deeper understanding of its behavior and capabilities.
"""
import os
from dotenv import load_dotenv

from workflow_agents.base_agents import DirectPromptAgent


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set")

prompt = "What is the Capital of France?"
direct_agent = DirectPromptAgent(openai_api_key)
direct_agent_response = direct_agent.respond(prompt)

print(direct_agent_response)

print("""\nThis response was generated using the DirectPromptAgent, which relies solely on the 
LLM's pre-trained knowledge without any additional context or retrieved information."""
)

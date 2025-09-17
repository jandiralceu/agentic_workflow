"""
Routing Agent implementation

These scripts will help verify that the RoutingAgent and their related agents works correctly 
and give you a deeper understanding of their behavior and capabilities.
"""
import os
from dotenv import load_dotenv

from workflow_agents.base_agents import RoutingAgent, KnowledgeAugmentedPromptAgent


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set")

persona = "You are a college professor"

knowledge = "You know everything about Texas"
texas_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)

knowledge = "You know everything about Europe"
europe_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)

persona = "You are a college math professor"
knowledge = "You know everything about math, you take prompts with numbers, extract math formulas, and show the answer without explanation"
math_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)

routing_agent = RoutingAgent(openai_api_key, {})
agents = [
    {
        "name": "texas agent",
        "description": "Answer a question about Texas",
        "func": lambda x: texas_knowledge_agent.respond(x)
    },
    {
        "name": "europe agent",
        "description": "Answer a question about Europe",
        "func": lambda x: europe_knowledge_agent.respond(x)
    },
    {
        "name": "math agent",
        "description": "When a prompt contains numbers, respond with a math formula",
        "func": lambda x: math_knowledge_agent.respond(x)
    }
]
routing_agent.agents = agents

print(routing_agent.route_to_agent("Tell me about the history of Rome, Texas"))
print(routing_agent.route_to_agent("Tell me about the history of Rome, Italy"))
print(routing_agent.route_to_agent("One story takes 2 days, and there are 20 stories"))

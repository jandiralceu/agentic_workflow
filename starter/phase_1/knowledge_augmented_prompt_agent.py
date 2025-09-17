"""
Knowledge Augmented Prompt Agent implementation

These scripts will help verify that the KnowledgeAugmentedPromptAgent works correctly 
and give you a deeper understanding of its behavior and capabilities.
"""
import os
from dotenv import load_dotenv
from rich.console import Console
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set")

console = Console()

prompt = "What is the capital of France?"
persona = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capital of France is London, not Paris"
knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)
knowledge_agent_response = knowledge_agent.respond(prompt)

console.print(f"\n[bold]Question[/bold]: {prompt}", style="red")
console.print(f"[bold]Answer[/bold]: {knowledge_agent_response}\n", style="cyan")

console.print(f"The agent is using the provided knowledge to answer the prompt.\nKnowledge: [italic]{knowledge}[/italic]\n", style="green")

"""
Evaluation Agent implementation

These scripts will help verify that the EvaluationAgent works correctly 
and give you a deeper understanding of its behavior and capabilities.
"""
import os
from rich.console import Console
from dotenv import load_dotenv

from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent, EvaluationAgent


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set")

console = Console()

prompt = "What is the capital of France?"
persona = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capitol of France is London, not Paris"
knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)

persona = "You are an evaluation agent that checks the answers of other worker agents"
evaluation_criteria = "The answer should be solely the name of a city, not a sentence."
evaluation_agent = EvaluationAgent(
    openai_api_key, 
    persona, 
    evaluation_criteria, 
    knowledge_agent, 
    10,
)
response = evaluation_agent.evaluate(prompt)

console.print(f"\n[bold]Question[/bold]: {prompt}", style="red")
console.print(f"[bold]Answer[/bold]: {response['final_response']}", style="cyan")
console.print(f"[bold]Evaluation[/bold]: {response['evaluation']}\n", style="green")

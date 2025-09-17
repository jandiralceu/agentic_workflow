"""
Augmented Prompt Agent implementation

These scripts will help verify that the AugmentedPromptAgent works correctly 
and give you a deeper understanding of its behavior and capabilities.
"""
import os
from dotenv import load_dotenv
from rich.console import Console

from workflow_agents.base_agents import AugmentedPromptAgent


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set")

console = Console()

prompt = "What is the capital of France?"
persona = "You are a college professor; your answers always start with: 'Dear students,'"
augmented_agent = AugmentedPromptAgent(openai_api_key, persona)
augmented_agent_response = augmented_agent.respond(prompt)

console.print(f"\n[bold]Question[/bold]: {prompt}", style="red")
console.print(f"[bold]Answer[/bold]: {augmented_agent_response}\n", style="cyan")


console.print("This response was generated using the [bold]AugmentedPromptAgent[/bold] with a college professor persona, utilizing the LLM's general knowledge within that academic context. The professor persona transformed the response by requiring it to begin with [italic]'Dear students,'[/italic] and frame the answer from an educational standpoint, making it sound like a classroom explanation rather than a casual response.\n")

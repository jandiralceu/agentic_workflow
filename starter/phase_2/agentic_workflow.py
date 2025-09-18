import os
from rich.console import Console
from dotenv import load_dotenv

from workflow_agents.base_agents import (
    ActionPlanningAgent, 
    KnowledgeAugmentedPromptAgent, 
    EvaluationAgent,
    RoutingAgent,
)

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set")

console = Console()

try:
    with open("Product-Spec-Email-Router.txt", "r") as file:
        product_spec = file.read()
except Exception as e:
    console.print(f"Error: Cannot read Product-Spec-Email-Router.txt - {e}", style="bold red")
    exit(1)

knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)

action_planning_agent = ActionPlanningAgent(openai_api_key, knowledge_action_planning)

persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome."
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    "Focus on the 'what' and 'why' rather than the 'how' - avoid technical implementation details."
    "Prioritize stories that deliver the most user value first."
    "Consider edge cases, error scenarios, and accessibility requirements where relevant."
    "Stories should be written from the user's perspective, not the system's perspective."
    f"{product_spec}"
)
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key, persona_product_manager, knowledge_product_manager
)

product_manager_evaluate_persona = "You are an expert Product Manager evaluation agent with deep knowledge of user story best practices."
evaluation_criteria_for_product_manager = """
ENHANCED USER STORY EVALUATION CRITERIA (Score each 0-10):

1. STRUCTURE (40%): Must follow "As a [user], I want [feature] so that [benefit]" format
2. SPECIFICITY (35%): Feature and user type must be concrete and implementable
3. VALUE (25%): Benefit must be clear and explain WHY the feature matters

SCORING:
- 9-10: Excellent quality
- 7-8: Good quality (passes threshold)
- 5-6: Needs improvement
- 0-4: Poor quality

Pass threshold: 7.0/10 (70%). Provide overall score and brief feedback for each dimension.
"""
product_manager_evaluation_agent = EvaluationAgent(
    openai_api_key,
    product_manager_evaluate_persona,
    evaluation_criteria_for_product_manager,
    product_manager_knowledge_agent,
    5
)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups."

program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key, persona_program_manager, knowledge_program_manager
)

persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."
evaluation_criteria_program_manager = ("The answer should be product features that follow the following structure: "
                                      "Feature Name: A clear, concise title that identifies the capability\n"
                                      "Description: A brief explanation of what the feature does and its purpose\n"
                                      "Key Functionality: The specific capabilities or actions the feature provides\n"
                                      "User Benefit: How this feature creates value for the user")
program_manager_evaluation_agent = EvaluationAgent(
    openai_api_key,
    persona_program_manager_eval,
    evaluation_criteria_program_manager,
    program_manager_knowledge_agent,
    5
)

persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story."
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key, persona_dev_engineer, knowledge_dev_engineer
)

persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
evaluation_criteria_dev_engineer = ("The answer should be tasks following this exact structure: "
                                   "Task ID: A unique identifier for tracking purposes\n"
                                   "Task Title: Brief description of the specific development work\n"
                                   "Related User Story: Reference to the parent user story\n"
                                   "Description: Detailed explanation of the technical work required\n"
                                   "Acceptance Criteria: Specific requirements that must be met for completion\n"
                                   "Estimated Effort: Time or complexity estimation\n"
                                   "Dependencies: Any tasks that must be completed first")
development_engineer_evaluation_agent = EvaluationAgent(
    openai_api_key,
    persona_dev_engineer_eval,
    evaluation_criteria_dev_engineer,
    development_engineer_knowledge_agent,
    5
)

routing_agent = RoutingAgent(openai_api_key, {})

def product_manager_support_function(query: str):
    response = product_manager_knowledge_agent.respond(query)
    evaluated_response = product_manager_evaluation_agent.evaluate(response)
    return evaluated_response["final_response"]

def program_manager_support_function(query: str):
    response = program_manager_knowledge_agent.respond(query)
    evaluated_response = program_manager_evaluation_agent.evaluate(response)
    return evaluated_response["final_response"]

def development_engineer_support_function(query: str):
    response = development_engineer_knowledge_agent.respond(query)
    evaluated_response = development_engineer_evaluation_agent.evaluate(response)
    return evaluated_response["final_response"]

agents = [
    {
        "name": "Product Manager",
        "description": "Responsible for defining product personas and user stories only. Does not define features or tasks. Does not group stories into features.",
        "func": lambda x: product_manager_support_function(x),
    },
    {
        "name": "Program Manager",
        "description": "Responsible for defining product features only. Does not define user stories or tasks. Does not break down features into tasks.",
        "func": lambda x: program_manager_support_function(x),
    },
    {
        "name": "Development Engineer",
        "description": "Responsible for defining development tasks only. Does not define user stories or features. Does not break down stories into tasks.",
        "func": lambda x: development_engineer_support_function(x),
    }
]

routing_agent.agents = agents

console.print("\n*** Workflow execution started ***\n", style="bold red")

workflow_prompts = [
    "What would the development tasks for this product be?",
    "Define only the key features for the Email Router product",
    "Generate a risk assessment plan for the Email Router based on its specification",
    "Create comprehensive user stories for the Email Router system"
]


for prompt in workflow_prompts:
    console.print(f"Task to complete in this workflow, workflow prompt = {prompt}", style="italic red")
    console.print("Defining workflow steps from the workflow prompt", style="bold red")

    try:
        workflow_steps = action_planning_agent.extract_steps_from_prompt(prompt)
        completed_steps = []

        for step in workflow_steps:
            try:
                result = routing_agent.route(step)
                completed_steps.append(result)
                console.print(f"\nStep: {step}", style="bold red")
                console.print(f"Result: {result}", style="italic green")
            except Exception as e:
                error_msg = f"Step failed: {step} - Error: {str(e)}"
                completed_steps.append(error_msg)
                console.print(f"\nStep: {step}", style="bold red")
                console.print(f"Result: {error_msg}", style="italic red")

        if completed_steps:
            console.print(f"\n\nFinal output of the workflow: {completed_steps[-1]}", style="bold blue")
        else:
            console.print(f"\n\nNo results generated for this workflow", style="bold red")

    except Exception as e:
        console.print(f"\nWorkflow failed: {str(e)}", style="bold red")

# TODO: 1 - Import EvaluationAgent and KnowledgeAugmentedPromptAgent classes
import os
from dotenv import load_dotenv
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent, EvaluationAgent


# Load environment variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set")

prompt = "What is the capital of France?"

# Parameters for the Knowledge Agent
persona = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capitol of France is London, not Paris"
# TODO: 2 - Instantiate the KnowledgeAugmentedPromptAgent here
knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)

# Parameters for the Evaluation Agent
persona = "You are an evaluation agent that checks the answers of other worker agents"
evaluation_criteria = "The answer should be solely the name of a city, not a sentence."
# TODO: 3 - Instantiate the EvaluationAgent with a maximum of 10 interactions here
evaluation_agent = EvaluationAgent(
    openai_api_key, 
    persona, 
    evaluation_criteria, 
    knowledge_agent, 
    3,
)

# TODO: 4 - Evaluate the prompt and print the response from the EvaluationAgent
evaluation_agent.evaluate(prompt)
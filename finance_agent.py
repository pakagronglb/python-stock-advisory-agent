from agno.agent import Agent
from agno.models.openai import OpenAIChat # for OpenAI models
# from agno.models.anthropic import Claude # for Anthropic models
from agno.tools.yfinance import YFinanceTools # pip install yfinance
from instruction_templates import agent_instructions_2
from agno.playground import Playground, serve_playground_app
import os
from dotenv import load_dotenv

load_dotenv()

def save_as_report(content: str, filename: str):
    """
    Save the generated report content to a file.

    Args:
        content (str): The content of the report.
        filename (str): The name of the file to save the report to.

    Returns:
        None
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        return 'File saved'
    except Exception as e:
        return str(e)
    
finance_agent = Agent(
    name='Finance Agent',
    model=OpenAIChat(
        id='gpt-4o',
        api_key=os.getenv('OPENAI_API_KEY')  # Add your API key here
    ),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
            historical_prices=True,
            company_info=True,
            company_news=True
        ),
        save_as_report
    ],
    instructions=agent_instructions_2,
    add_history_to_messages=True,
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,    
)

# CLI Setup
# while True:
#     user_input = input("You: ")
#     if user_input.lower() == 'exit':
#         break
#     response = finance_agent.run(user_input)
#     print(response.content)

# Playground Setup
app = Playground(agents=[finance_agent]).get_app()

if __name__ == '__main__':
    serve_playground_app('finance_agent:app', reload=True)
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.agents import AgentExecutor, Tool, create_react_agent
from dotenv import load_dotenv
from tools.tools import get_profile_url

load_dotenv()


def lookup(name):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    template = """
    Answer the following questions as best you can.
    You have access to the following tools:{tools}
    Use the following format:
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    Begin!
    Question: 
    Given the full name {name_of_person} I want you to give me a link to their LinkedIn profile page.
                    Your answer should only contain a url.
    Thought:{agent_scratchpad}"""

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 LinkedIn profile page",
            func=get_profile_url,
            description="useful for when you need to get the LinkedIn profile page url",
        )
    ]

    prompt_template = PromptTemplate(
        template=template, input_variables=['name_of_person', 'agent_scratchpad', 'tool_names', 'tools'])

    agent = create_react_agent(llm=llm,tools=tools_for_agent, prompt=prompt_template)
    agent_executor = AgentExecutor(agent=agent,tools=tools_for_agent, verbose=True, handle_parsing_errors=True)

    
    linkedin_profile_url = agent_executor.invoke({"name_of_person":name})
    return linkedin_profile_url

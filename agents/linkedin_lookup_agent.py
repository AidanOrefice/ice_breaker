from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, Tool, AgentType
from dotenv import load_dotenv
from tools.tools import get_profile_url

load_dotenv()


def lookup(name):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    template = """Given the full name {name_of_person} I want you to give me a link to their LinkedIn profile page.
                    Your answer should only contain a url."""

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 LinkedIn profile page",
            func=get_profile_url,
            description="useful for when you need to get the LinkedIn profile page url",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    linkedin_profile_url = agent.run(prompt_template.format_prompt(name_of_person=name))
    return linkedin_profile_url

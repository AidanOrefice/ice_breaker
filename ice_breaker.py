from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

load_dotenv()


if __name__ == "__main__":
    print("Hello LangChain!")

    summary_template = """
        given the LinkedIn information {information} about a person from I want you to create:
        1. A short summary
        2. two interesting facts about them

    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    linkedin_profile_url = linkedin_lookup_agent(name="Aidan Orefice Kubrick")
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    result = chain.invoke({"information": linkedin_data})
    print(result["text"])

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_parties.linkedin import scrape_linkedin_profile
from output_parsers import person_intel_parser


def ice_break(name):
    print("Hello LangChain!")
    summary_template = """
         given the Linkedin information {linkedin_information} about a person from I want you to create:
         1. a short summary
         2. two interesting facts about them
         3. A topic that may interest them
         4. 2 creative Ice breakers to open a conversation with them 
                    \n{format_instructions}

    """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    linkedin_profile_url = linkedin_lookup_agent(name="Aidan Orefice")
    print(linkedin_profile_url)
    #linkedin_data = scrape_linkedin_profile(linkedin_profile_url=str(linkedin_profile_url['output']))
    #print(linkedin_data)

    result = chain.run(linkedin_information= linkedin_data)

    return person_intel_parser.parse(result["text"]), linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    name = "Aidan Orefice"
    result = ice_break(name)
    print(result)

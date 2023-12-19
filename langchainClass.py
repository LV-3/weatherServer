from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
from dotenv import load_dotenv
import os


class CommaSeparatedListOutputParser(BaseOutputParser):
    def parse(self, text: str):
        return text.strip().split(", ")


class ExtractWord:
    def __init__(self) -> None:
        load_dotenv()
        
        self.openai_api_key=os.getenv("OPEN_API_KEY")
        self.llm = OpenAI(openai_api_key=self.openai_api_key)
        self.templates = {
            'template': 
            """
                Today's weather is {SKY}, {PTY} I wonder what kind of atmosphere and genre of movie would be good to watch. Extract words for atmosphere and genre.

                Separate each mood word with a comma (,) and refrain from adding any additional information.
            """
        }

    # '-' 문자를 제외한 나머지 특수문자는 삭제하고, 단어는 소문자로 통일
    def clean_word(self, text: str) -> str:
        import re
        pattern = re.compile(r'[^A-Za-z-]')
        cleaned_text = pattern.sub('', text)
        cleaned_text_lower = cleaned_text.lower()
        return cleaned_text_lower

    def run_llm_chain(self, SKY_var: str, PTY_var: str, llm_openai_api_key:str, template:str) -> list[str]:
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = ""
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        chat_prompt.format_messages(SKY=SKY_var, PTY=PTY_var)

        chain = LLMChain(
            llm=ChatOpenAI(openai_api_key=llm_openai_api_key),
            prompt=chat_prompt,
            output_parser=CommaSeparatedListOutputParser()
        )

        results = chain.run(SKY=SKY_var,PTY=PTY_var)

        # 20글자 이하인 것만 남음
        # results = [result for result in results if len(result) <= 20]
        # results = [self.clean_word(result) for result in results if 2 <= len(self.clean_word(result)) <= 20]
        return results
    


    def run(self, SKY: str, PTY: str) -> list[str]:
        if PTY == "없음": PTY = ""

        result = self.run_llm_chain(SKY_var=SKY, PTY_var=PTY, llm_openai_api_key=self.openai_api_key, template=self.templates.get("template"))
        print('result', result)
        return result
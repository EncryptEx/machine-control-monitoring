from langchain_ollama import ChatOllama
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough
)
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate


class LLM():
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2",
            temperature=0.1,
            base_url=f"http://ollama:11434"
        )

    def ask(self, question, info):

        prompt_str = "You are a machine assistant, the user has made the question: {question} and you have the info: {info} answer que users query"

        prompt = ChatPromptTemplate.from_template(prompt_str)


        chain =  prompt | self.llm | StrOutputParser()

        response = chain.invoke({"question": question, "info": info})

        user_response, action = self.parse_response(response)
        return response, action
    
    def parse_response(self, response):
        return response

from langchain_ollama import ChatOllama
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough
)
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate


llm = ChatOllama(
    model="llama3.2",
    temperature=0.1,
    base_url=f"http://localhost:11434"
)



prompt_str = "Hi! {question}"

prompt = ChatPromptTemplate.from_template(prompt_str)

question = "How are you"

chain = RunnableParallel({ "question": RunnablePassthrough()}) | prompt | llm | StrOutputParser()
response = chain.invoke(question)

print(response)

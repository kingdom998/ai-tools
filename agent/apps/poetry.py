import sys
import os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from util._llm import llm
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser


def make_poetry(topic):
    prompt = ChatPromptTemplate.from_template("请为我写一首关于 {topic}的诗。")
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    return chain.invoke({"topic": topic})


if __name__ == "__main__":
    print(make_poetry("夏天"))

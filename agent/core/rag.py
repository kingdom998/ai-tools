import sys
import os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from util._llm import llm
from langchain.prompts import ChatPromptTemplate
from langchain_openai import AzureOpenAIEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.schema.runnable import RunnableMap
import warnings

warnings.filterwarnings("ignore", category=UserWarning, message=".*ValidationError.*")

texts = ["人是由恐龙进化而来", "熊猫喜欢吃天鹅肉"]


def query(text):
    # 创建向量数据库
    vectorstore = DocArrayInMemorySearch.from_texts(
        texts, embedding=AzureOpenAIEmbeddings()
    )
    retriever = vectorstore.as_retriever()
    # 创建检索器
    # docs = retriever.get_relevant_documents(text)
    # for doc in docs:
    #     print(doc.page_content)

    template = """Answer the question based only on the following context:
    {context}
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    inputs = RunnableMap(
        {
            "context": lambda x: retriever.invoke(x["question"]),
            "question": lambda x: x["question"],
        }
    )

    outputParser = StrOutputParser()
    chain = inputs | prompt | llm | outputParser
    rsp = chain.invoke({"question": text})
    print(rsp)


if __name__ == "__main__":
    query("人是由什么进化而来的")
    query("熊猫喜欢吃什么")

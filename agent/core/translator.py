import sys
import os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from util._llm import llm
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个助手，直接将用户所输入的从 {input_language} 翻译到 {output_language}.",
        ),
        ("human", "{input}"),
    ]
)


def translate(text, input_language, output_language):
    try:
        content = {
            "input_language": input_language,
            "output_language": output_language,
            "input": text,
        }
        chain = prompt | llm | StrOutputParser()
        rsp = chain.invoke(content)
        return rsp
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    while True:
        try:
            text = input("请输入要翻译的内容：")
            translation = translate(text, "chinese", "english")
            print("译文：", translation)
        except EOFError:
            print("\n你输入 Ctrl+D 即将退出")
            break
        except KeyboardInterrupt:
            print("\n你输入 Ctrl+C 即将退出")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

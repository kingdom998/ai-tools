
import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = AzureChatOpenAI(
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    openai_api_version="2024-12-01-preview",  # 根据你的 Azure OpenAI 版本调整
)

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
        chain = prompt | llm
        resp = chain.invoke(content)
        return resp.content
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


# Example usage
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

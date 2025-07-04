import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool


load_dotenv(override=True)
deploy_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
print(f"Using Azure OpenAI deployment: {deploy_name}, api_key: {api_key}, endpoint: {endpoint}\n")
llm = AzureChatOpenAI(deployment_name=deploy_name, openai_api_key=api_key, azure_endpoint=endpoint)


@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    print(f"add({a}, {b})")

    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b


@tool
def img_resize(w: int, h: int) -> int:
    """Resizes an image to the given width and height."""
    print(f"img_resize({w}, {h})")
    return w * h


@tool
def img2img(w: int, h: int) -> int:
    """generates an image from a given width and height."""
    print(f"img2img({w}, {h})")
    return w * h


def call_tool(chain, query="resize an image to 100x200"):
    rsp = chain.invoke({"input": query})
    print("rsp: ", rsp)
    for tool_call in rsp.additional_kwargs.get("tool_calls", []):
        print("tool_call: ", tool_call)
        func = tool_call.get("function")
        if not func:
            continue
        name = func.get("name")
        args = func.get("arguments")
        args = eval(args)
        tool_function = globals().get(name)
        print(tool_function.invoke(input=args))


def test():
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages([("system", "You are a helpful assistant"), ("user", "{input}")])

    tools = [add, multiply, img_resize]
    llm_with_tools = llm.bind_tools(tools)

    chain = prompt | llm_with_tools
    while True:
        try:
            query = input("Enter a query: ")
            if query == "exit":
                break
            call_tool(chain, query)
        except EOFError:
            print("\n你输入 Ctrl+D 即将退出")
            break
        except KeyboardInterrupt:
            print("\n你输入 Ctrl+C 即将退出")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break


if __name__ == "__main__":
    test()

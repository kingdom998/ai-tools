import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool


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


def route(result):
    if isinstance(result, AgentFinish):
        return result.return_values["output"]
    else:
        tools = {
            "add": add,
            "multiply": multiply,
        }
        return tools[result.tool].run(result.tool_input)


load_dotenv()

llm = AzureChatOpenAI(
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


if __name__ == "__main__":
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages([("system", "You are a helpful assistant"), ("user", "{input}")])

    tools = [add, multiply, img_resize]
    llm_with_tools = llm.bind_tools(tools)

    chain = prompt | llm_with_tools
    while True:
        query = input("Enter a query: ")
        if query == "exit":
            break
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
    # query = "resize an image to 100x200"
    # rsp = chain.invoke({"input": query})
    # for tool_call in rsp.additional_kwargs.get("tool_calls", []):
    #     print("tool_call: ", tool_call)
    #     func = tool_call.get("function")
    #     if not func:
    #         continue
    #     name = func.get("name")
    #     args = func.get("arguments")
    #     args = eval(args)
    #     tool_function = globals().get(name)
    #     print(tool_function.invoke(input=args))

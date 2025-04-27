import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from langchain.schema.agent import AgentFinish


load_dotenv()

llm = AzureChatOpenAI(
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b


def route(result):
    if isinstance(result, AgentFinish):
        return result.return_values["output"]
    else:
        tools = {
            "add": add,
            "multiply": multiply,
        }
        return tools[result.tool].run(result.tool_input)


if __name__ == "__main__":
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages(
        [("system", "You are a helpful assistant"), ("user", "{input}")]
    )

    tools = [add, multiply]
    llm_with_tools = llm.bind_tools(tools)

    chain = prompt | llm_with_tools
    query = "What is 3 * 12? Also, what is 11 + 49?"
    rsp = chain.invoke({"input": query})
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

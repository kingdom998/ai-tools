import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util._llm import llm
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain.schema.agent import AgentFinish
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


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


memory = MemorySaver()
tools = [add, img2img]
agent_executor = create_react_agent(llm, tools, checkpointer=memory)
# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
while True:
    content = input("请输入：")
    response = agent_executor.invoke(
        {"messages": [HumanMessage(content=content)]}, config=config
    )
    output = response["messages"][-1]
    print(output.content, output)

# for step in agent_executor.stream(
#     {"messages": [HumanMessage(content="生成图片")], "config": config},
#     config,
#     stream_mode="values",
# ):
#     step["messages"][-1].pretty_print()

if __name__ == "__main__":
    while True:
        try:
            content = input("请输入：")
            if content.lower() == "exit":
                break
            response = agent_executor.invoke(
                {"messages": [HumanMessage(content=content)]}, config=config
            )
            output = response["messages"][-1]
            print(output.content, output)
        except EOFError:
            print("\n你输入 Ctrl+D 即将退出")
            break
        except KeyboardInterrupt:
            print("\n你输入 Ctrl+C 即将退出")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break
#         print("tool_call: ", tool_call)
#             func = tool_call.get("function")

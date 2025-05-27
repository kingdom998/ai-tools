import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core._llm import llm
from langchain.agents import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent


@tool
def req_weather(location: str) -> str:
    """获取指定城市的天气信息（模拟函数）"""
    return f"{location}的天气：晴天，25°C"


tools = [req_weather]
agent = create_react_agent(llm, tools)


def query_weather(location):
    """查询指定城市的天气"""
    return agent.invoke(
        {
            "messages": [HumanMessage(content=f"请问{location}的天气如何？")],
            "config": {"configurable": {"thread_id": "abc123"}},
        }
    )


def test():
    while True:
        try:
            location = input("请输入城市名称：")
            if location.lower() == "exit":
                break
            weather_info = query_weather(location)
            print(weather_info)
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

from _llm import llm
from langchain.agents import tool
from langchain.agents import AgentType, initialize_agent


@tool
def get_weather(location: str) -> str:
    """获取指定城市的天气信息（模拟函数）"""
    return f"{location}的天气：晴天，25°C"


tools = [get_weather]

# 初始化 Agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
rsp = agent.invoke("请告诉我北京的天气")
print(rsp)

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils._llm import llm
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Sequence
from typing_extensions import Annotated, TypedDict


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str


prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


def call_model(state: State):
    prompt = prompt_template.invoke(state)
    response = llm.invoke(prompt)
    return {"messages": [response]}


memory = MemorySaver()
workflow = StateGraph(state_schema=State)
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)
app = workflow.compile(checkpointer=memory)


def one():
    config = {"configurable": {"thread_id": "abc123"}}

    query = "Hi! I'm Bob."
    language = "Chinese"

    input_messages = [HumanMessage(query)]
    output = app.invoke({"messages": input_messages, "language": language}, config)
    output["messages"][-1].pretty_print()

    query = "What is my name?"

    input_messages = [HumanMessage(query)]
    output = app.invoke(
        {"messages": input_messages},
        config,
    )
    output["messages"][-1].pretty_print()

if __name__ == "__main__":
    one()
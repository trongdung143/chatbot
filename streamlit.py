import streamlit as st
import asyncio
import uuid
import importlib
import sys, os
from langchain_core.messages import HumanMessage, AIMessage


st.set_page_config(page_title="Multi-Agent", page_icon="", layout="wide")


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


st.markdown(
    """
    <style>
    .stApp {
        background-color: #f9fafb;
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 8px;
    }
    .stChatMessage.user {
        background-color: #dbeafe;
        text-align: right;
    }
    .stChatMessage.assistant {
        background-color: #f3f4f6;
    }
    .stTextInput input {
        border-radius: 12px;
        border: 1px solid #9ca3af;
        padding: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


AGENTS_DIR = "src/agents"
agents = sorted(
    [
        name
        for name in os.listdir(AGENTS_DIR)
        if os.path.isdir(os.path.join(AGENTS_DIR, name))
    ]
)

agent_icons = {
    "analyst": "📊",
    "assigner": "📌",
    "calculator": "🧮",
    "coder": "💻",
    "memory": "🧠",
    "planner": "🗓️",
    "search": "🔍",
    "supervisor": "👨‍💼",
    "tool": "🛠️",
    "vision": "👁️",
    "writer": "✍️",
}

with st.sidebar:
    st.title("Multi-Agent Chatbot")
    st.markdown("### Agents")

    for agent in agents:
        icon = agent_icons.get(agent, "🔹")
        st.markdown(f"- {icon} **{agent.capitalize()}**")

    st.divider()

if "event_loop" not in st.session_state:
    loop = asyncio.new_event_loop()
    st.session_state.event_loop = loop
    asyncio.set_event_loop(loop)
else:
    asyncio.set_event_loop(st.session_state.event_loop)

if "graph" not in st.session_state:
    workflow_mod = importlib.import_module("src.agents.workflow")
    st.session_state.graph = workflow_mod.graph

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    avatar = "🧑‍💻" if role == "user" else "🤖"
    with st.chat_message(role, avatar=avatar):
        st.markdown(msg.content)


def run_on_session_loop(coro):
    loop = st.session_state.event_loop
    return loop.run_until_complete(coro)


if prompt := st.chat_input("Nhập tin nhắn..."):
    st.chat_message("user", avatar="🧑‍💻").markdown(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))

    input_state = {
        "messages": [HumanMessage(content=prompt)],
        "thread_id": st.session_state.thread_id,
        "next_agent": None,
        "prev_agent": None,
        "task": None,
        "result": None,
        "human": None,
    }
    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        full_response = [""]

        async def run_graph():
            async for event in st.session_state.graph.astream(
                input=input_state,
                config=config,
                stream_mode=["messages", "updates"],
                subgraphs=True,
            ):
                _, data_type, chunk = event
                if data_type == "messages":
                    msg, meta = chunk
                    agent = meta.get("langgraph_node", "unknown")
                    if agent in ["memory", "supervisor", "assigner"]:
                        continue
                    text = (
                        msg.content
                        if isinstance(msg.content, str)
                        else str(msg.content)
                    )
                    full_response[0] += text
                    placeholder.markdown(full_response[0])

        with st.spinner("💡 Đang suy nghĩ..."):
            run_on_session_loop(run_graph())

        st.session_state.messages.append(AIMessage(content=full_response[0]))

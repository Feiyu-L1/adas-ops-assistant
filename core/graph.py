import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from agents.triage import TriageAgent
from agents.log import LogAgent
from agents.doc import DocAgent
from agents.response import ResponseAgent
from agents.escalation import EscalationAgent
from core.message import Message
from core.model_adapter import MimoAdapter
from core.message_bus import MessageBus
from core.knowledge_store import MockStore
from config import get_triage_adapter, get_adapter
load_dotenv()

class AgentState(TypedDict):
    message: str
    history: list 
    intent: str
    thinking: dict
    analysis: str
    report: str
    escalation: str

graph = StateGraph(AgentState)

api_key = os.getenv("MIMO_API_KEY")
triage_adapter = get_triage_adapter()
adapter = get_adapter()
bus = MessageBus()
store = MockStore()

triage_agent = TriageAgent(triage_adapter, bus, store)
log_agent = LogAgent(adapter, bus, store)
doc_agent = DocAgent(adapter, bus, store)
response_agent = ResponseAgent(adapter, bus, store)
escalation_agent = EscalationAgent(adapter, bus, store)

def triage_node(state):
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in state["history"]])
    prompt = f"历史对话：\n{history_text}\n\n当前问题：{state['message']}"
    msg = Message(sender="user", receiver="triage", type="question", content=prompt)
    data = triage_agent.process(msg)
    return {"intent": data["intent"], "thinking": {"triage": data["thinking"]}}

def log_node(state):
    msg = Message(sender="user", receiver="log", type="analysis", content=state["message"])
    data = log_agent.process(msg)
    return {"analysis": data, "thinking": {"log": data["thinking"]}}

def doc_node(state):
    msg = Message(sender="user", receiver="doc", type="analysis", content=state["message"])
    data = doc_agent.process(msg)
    return {"analysis": data["answer"], "thinking": {"doc": data["thinking"]}}

def response_node(state):
    msg = Message(sender="user", receiver="response", type="report", content=state["analysis"])
    data = response_agent.process(msg)
    return {"report": data["report"], "thinking": {"response": data["thinking"]}}

def escalation_node(state):
    msg = Message(sender="user", receiver="escalation", type="report", content=state["report"])
    data = escalation_agent.process(msg)
    return {"escalation": data["escalation"], "thinking": {"escalation": data["thinking"]}}

graph.add_node("triage", triage_node)
graph.add_node("log", log_node)
graph.add_node("doc", doc_node)
graph.add_node("response", response_node)
graph.add_node("escalation", escalation_node)

graph.add_edge(START, "triage")
def route_by_intent(state):
    if state["intent"] in ["日志异常", "性能问题"]:
        return "log"
    else:
        return "doc"
graph.add_conditional_edges("triage", route_by_intent)
graph.add_edge("log", "response")
graph.add_edge("doc", END)               # ← doc 直接结束
graph.add_edge("response", "escalation")
graph.add_edge("escalation", END)

app = graph.compile()
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
from core.knowledge_store import MockStore, DifyStore
from config import get_triage_adapter, get_adapter, DIFY_API_KEY, DIFY_DATASET_ID, USE_DIFY_STORE
load_dotenv()

class AgentState(TypedDict):
    message: str
    history: list 
    intent: str
    thinking: dict
    analysis: str
    report: str
    escalation: str
    sources: list

graph = StateGraph(AgentState)

triage_adapter = get_triage_adapter()
adapter = get_adapter()
if USE_DIFY_STORE:
    store = DifyStore(DIFY_API_KEY, DIFY_DATASET_ID)
else:
    store = MockStore()

triage_agent = TriageAgent(triage_adapter, store)
log_agent = LogAgent(adapter, store)
doc_agent = DocAgent(adapter, store)
response_agent = ResponseAgent(adapter, store)
escalation_agent = EscalationAgent(adapter, store)

def triage_node(state):
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in state["history"]])
    prompt = f"历史对话：\n{history_text}\n\n当前问题：{state['message']}"
    msg = Message(sender="user", receiver="triage", type="question", content=prompt)
    data = triage_agent.process(msg)
    return {"intent": data.get("intent", ""), "thinking": {"triage": data.get("thinking", "")}}

LOG_KEY_LABELS = {
    "error_type": "错误类型",
    "time_pattern": "时间模式",
    "impact_scope": "影响范围",
    "severity": "严重程度",
    "suggestion": "建议处理",
}

def log_node(state):
    msg = Message(sender="user", receiver="log", type="analysis", content=state["message"])
    data = log_agent.process(msg)
    parts = []
    for key, value in data.items():
        if key not in ("thinking", "sources"):
            label = LOG_KEY_LABELS.get(key, key)
            parts.append(f"{label}: {value}")
    analysis_text = "\n".join(parts)

    return {
        "analysis": analysis_text,
        "thinking": {"log": data.get("thinking", "")},
        "sources": data.get("sources", [])
    }

def doc_node(state):
    msg = Message(sender="user", receiver="doc", type="analysis", content=state["message"])
    data = doc_agent.process(msg)
    return {
        "analysis": data.get("answer", ""), 
        "thinking": {"doc": data.get("thinking", "")},
        "sources": data.get("sources", [])}

def response_node(state):
    msg = Message(sender="user", receiver="response", type="report", content=state["analysis"])
    data = response_agent.process(msg)
    return {"report": data.get("report", ""), "thinking": {"response": data.get("thinking", "")}}

def escalation_node(state):
    msg = Message(sender="user", receiver="escalation", type="report", content=state["report"])
    data = escalation_agent.process(msg)
    return {"escalation": data.get("escalation", ""), "thinking": {"escalation": data.get("thinking", "")}}

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
graph.add_edge("doc", END)
graph.add_edge("response", "escalation")
graph.add_edge("escalation", END)

app = graph.compile()
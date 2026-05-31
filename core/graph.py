from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from unittest.mock import MagicMock
from agents.triage import TriageAgent
from agents.log import LogAgent
from agents.doc import DocAgent
from agents.response import ResponseAgent
from agents.escalation import EscalationAgent
from core.message import Message

class AgentState(TypedDict):
    message: str
    intent: str
    analysis: str
    report: str
    escalation: str

graph = StateGraph(AgentState)

mock_adapter = MagicMock()
mock_bus = MagicMock()
mock_store = MagicMock()

triage_agent = TriageAgent(mock_adapter, mock_bus, mock_store)
log_agent = LogAgent(mock_adapter, mock_bus, mock_store)
doc_agent = DocAgent(mock_adapter, mock_bus, mock_store)
response_agent = ResponseAgent(mock_adapter, mock_bus, mock_store)
escalation_agent = EscalationAgent(mock_adapter, mock_bus, mock_store)

def triage_node(state):
    msg = Message(sender="user", receiver="triage", type="question", content=state["message"])
    result = triage_agent.process(msg)
    return {"intent": result}

def log_node(state):
    msg = Message(sender="user", receiver="log", type="analysis", content=state["message"])
    result = log_agent.process(msg)
    return {"analysis": result}

def doc_node(state):
    msg = Message(sender="user", receiver="doc", type="analysis", content=state["message"])
    result = doc_agent.process(msg)
    return {"analysis": result}

def response_node(state):
    msg = Message(sender="user", receiver="response", type="report", content=state["analysis"])
    result = response_agent.process(msg)
    return {"report": result}

def escalation_node(state):
    msg = Message(sender="user", receiver="escalation", type="report", content=state["report"])
    result = escalation_agent.process(msg)
    return {"escalation": result}

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
graph.add_edge("doc", "response")
graph.add_edge("response", "escalation")
graph.add_edge("escalation", END)

app = graph.compile()
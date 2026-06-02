import streamlit as st
from core.graph import app as graph_app

st.title("ADAS 智能运维助手")
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("请输入运维问题：")

if user_input:
    st.chat_message("user").write(user_input)
    with st.spinner("正在分析..."):
        result = graph_app.invoke({
        "message": user_input,
        "history": st.session_state.history
    })
    
    if "thinking" in result:
        for agent, thought in result["thinking"].items():
            with st.expander(f"🤔 {agent} Agent 思考过程"):
                st.write(thought)
                    
    st.write("### 意图分类")
    st.write(result.get("intent", ""))

    if result.get("intent") in ["日志异常", "性能问题"]:
        st.write("### 日志分析")
        st.write(result.get("analysis", ""))

        st.write("### 故障报告")
        st.write(result.get("report", ""))
    else:
        st.write("### 文档回答")
        st.write(result.get("analysis", ""))
        
    sources = result.get("sources", [])
    if sources:
        st.write("### 📄 参考来源")
        for i, doc in enumerate(sources, 1):
            st.write(f"{i}. {doc.get('name', '')}")
            content = doc.get("content", "")
            st.write(content[:500] + "..." if len(content) > 500 else content)

    if result.get("escalation") == "需要升级":
        st.write("### ⚠️ 升级判断")
        st.write("需要人工介入")

    if result.get("intent") in ["日志异常", "性能问题"]:
        assistant_content = result.get("report", "")
    else:
        assistant_content = result.get("analysis", "")
    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.history.append({"role": "assistant", "content": assistant_content})

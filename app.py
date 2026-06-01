import streamlit as st
from core.graph import app as graph_app

st.title("ADAS 智能运维助手")
user_input = st.chat_input("请输入运维问题：")

if user_input:
    st.chat_message("user").write(user_input)
    with st.spinner("正在分析..."):
        result = graph_app.invoke({"message": user_input})
    st.write("### 意图分类")
    st.write(result["intent"])


    if result["intent"] in ["日志异常", "性能问题"]:
        st.write("### 日志分析")
        st.write(result["analysis"])

        st.write("### 故障报告")
        st.write(result["report"])
    else:
        st.write("### 文档回答")
        st.write(result["analysis"])

    if result.get("escalation") == "需要升级":
        st.write("### ⚠️ 升级判断")
        st.write("需要人工介入")
    
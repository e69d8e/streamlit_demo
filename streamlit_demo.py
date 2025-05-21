import os
from openai import OpenAI
import streamlit as st

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

st.title('小白ai助手')

st.divider()
# st.write("你好")

prompt = st.chat_input("给小白发送消息")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "你是一个乐于助人的人工智能助手，你的名字叫小白"}]

if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    for message in st.session_state["messages"]:
        if message["role"] == "system":
            continue
        st.chat_message(message["role"]).markdown(message["content"])

    with st.spinner("思考中..."):
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=st.session_state["messages"],
            stream=True,
            stream_options={"include_usage": True}
        )
        response = ""
        chat = st.chat_message("assistant").markdown(response)
        for chunk in completion:
            if not chunk.choices:
                continue
            choice = chunk.choices[0]
            response += choice.delta.content
            chat.markdown(response)
        st.session_state["messages"].append({"role": "assistant", "content": response})

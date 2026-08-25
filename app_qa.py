import streamlit as st

import config_data as config


st.set_page_config(page_title="智能客服", page_icon="🤖")

# 标题
st.title("智能客服")
st.divider()            # 分隔符

if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "你好，有什么可以帮助你？"}]

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 在页面最下方提供用户输入栏
prompt = st.chat_input("请输入你的问题")

if prompt:

    # 在页面输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    ai_res_list = []
    with st.spinner("AI思考中..."):
        try:
            # RAG 依赖的模型与向量库初始化较慢。只在第一次提问时初始化，
            # 避免启动页面时只渲染出标题，看起来像前端内容丢失。
            if "rag" not in st.session_state:
                from rag import RagService

                st.session_state["rag"] = RagService()

            res_stream = st.session_state["rag"].chain.stream(
                {"input": prompt}, config.session_config
            )

            def capture(generator, cache_list):
                for chunk in generator:
                    cache_list.append(chunk)
                    yield chunk

            st.chat_message("assistant").write_stream(capture(res_stream, ai_res_list))
            st.session_state["message"].append(
                {"role": "assistant", "content": "".join(ai_res_list)}
            )
        except Exception as exc:
            st.chat_message("assistant").error(
                "服务初始化或回答失败，请检查 DASHSCOPE_API_KEY、网络连接和向量库配置。"
            )
            with st.expander("查看错误详情"):
                st.exception(exc)

# ["a", "b", "c"]   "".join(list)    -> abc
# ["a", "b", "c"]   ",".join(list)    -> a,b,c

"""Streamlit page for uploading txt files into the local vector store."""

import time

import streamlit as st

from knowledge_base import KnowledgeBaseService


def decode_text_file(file_bytes: bytes) -> tuple[str, str]:
    """Try common encodings used by txt files on Windows/Chinese systems."""
    candidate_encodings = ("utf-8", "utf-8-sig", "gbk", "gb2312", "gb18030")

    for encoding in candidate_encodings:
        try:
            return file_bytes.decode(encoding), encoding
        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError(
        "decode_text_file",
        file_bytes,
        0,
        1,
        "unsupported text encoding, tried utf-8/utf-8-sig/gbk/gb2312/gb18030",
    )


st.title("知识库文件上传")

uploader_file = st.file_uploader(
    "请选择 txt 文件",
    type=["txt"],
    accept_multiple_files=False,
)

if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()


if uploader_file is not None:
    file_name = uploader_file.name
    file_type = uploader_file.type or "text/plain"
    file_size = uploader_file.size / 1024

    st.subheader(f"文件名称：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")

    file_bytes = uploader_file.getvalue()

    try:
        text, detected_encoding = decode_text_file(file_bytes)
    except UnicodeDecodeError:
        st.error("文件解码失败：请将 txt 文件保存为 UTF-8、UTF-8 with BOM 或 GBK 后重试。")
        st.stop()

    st.caption(f"已识别文件编码：{detected_encoding}")

    with st.spinner("载入知识库中..."):
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)

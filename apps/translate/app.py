import streamlit as st
import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(parent_dir))
from libs.core.translator import translate

def do_translate(text, input_language, output_language):
    st.session_state.translation = translate(text, input_language, output_language)

cols = st.columns(2)
with cols[0]:
    input_language = st.selectbox("输入语言", ["chinese", "english"])
    original_text = st.text_area(
        "原文",
        key="original_text",
        placeholder="请输入要翻译的内容",
        height=800,
    )
with cols[1]:
    output_language = st.selectbox("输出语言", ["chinese", "english"])
    st.text_area(
        "译文",
        key="translation",
        placeholder="请输入要翻译的内容",
        height=800,
    )
st.button(
    "翻译",
    on_click=do_translate,
    args=[original_text, input_language, output_language],
    use_container_width=True,
)
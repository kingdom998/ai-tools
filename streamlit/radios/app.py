import sys
import os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
import streamlit as st
from utils.util import default_prompt, default_url, null_url, call_req

tool = st.radio("工具", options=["img2img", "img2video"])
st.session_state.current_tool = tool
st.write(f"你选择了 {tool} 工具")
prompt = st.text_input("prompt", placeholder=default_prompt)
img_url = st.text_input("img url", placeholder=default_url) or default_url
col1, col2 = st.columns([1, 1])
with col1:
    st.text("原始图片")
    st.image(img_url, width=400)
with col2:
    st.text("生成结果")
    is_video = st.session_state.current_tool == "img2video"
    result_key = "generated_videos" if is_video else "generated_imgs"
    urls = st.session_state.get(result_key, "")
    urls = [null_url] if not is_video and not urls else urls
    if is_video:
        if len(urls) > 0:
            st.video(urls[0])
    else:
        st.image(urls, width=400)

st.button(
    "提交",
    on_click=call_req,
    args=[prompt, img_url, st.session_state.current_tool == "img2video"],
    use_container_width=True,
)

import sys
import os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)

import streamlit as st
from utils.util import default_prompt, default_url, null_url, call_req


def display_input_tab(is_video=False):
    suffix = "video" if is_video else "img"
    prompt = st.text_input("prompt", key="prompt_"+ suffix, placeholder=default_prompt)
    img_url = (
        st.text_input("img url", key="img_" + suffix, placeholder=default_url)
        or default_url
    )
    col1, col2 = st.columns([1, 1])
    with col1:
        st.text("原始图片")
        st.image(img_url, width=400)
    with col2:
        st.text("生成结果")
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
        key="submit" + ("2" if is_video else ""),
        on_click=call_req,
        args=[prompt, img_url, is_video],
        use_container_width=True,
    )


tab1, tab2 = st.tabs(["图生图", "图生视频"])
with tab1:
    display_input_tab(is_video=False)

with tab2:
    display_input_tab(is_video=True)

import sys
import os
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(path)
sys.path.append(path)
import streamlit as st
from dashscope import ImageSynthesis, VideoSynthesis
from utils.util import req_synthesis, default_prompt, default_url, null_url


# 生成图像请求
def call_req(prompt, img_url):
    if st.session_state.selected_feature == "img2video":
        urls, tm, err = req_synthesis(
            call_func=VideoSynthesis.call,
            model=VideoSynthesis.Models.wanx_2_1_t2v_turbo,
            prompt=prompt,
            img_url=img_url,
            is_video=True,
        )
    else:
        urls, tm, err = req_synthesis(
            call_func=ImageSynthesis.call,
            model=ImageSynthesis.Models.wanx_v1,
            prompt=prompt,
            img_url=img_url,
            style="<3d cartoon>",
            is_video=False,
        )
    if err:
        st.error(err)
        return None

    if not urls:
        return
    if is_video:
        st.session_state.generated_videos = urls
    else:
        st.session_state.generated_imgs = urls


feature = st.radio("功能", options=["img2img", "img2video"])
st.session_state.selected_feature = feature
st.write(f"你选择了 {feature} 功能")
prompt = st.text_input("prompt", placeholder=default_prompt)
img_url = st.text_input("img url", placeholder=default_url) or default_url
col1, col2 = st.columns([1, 1])
with col1:
    st.text("原始图片")
    st.image(img_url, width=400)
with col2:
    st.text("生成结果")
    is_video = st.session_state.selected_feature == "img2video"
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
    args=[prompt, img_url],
    use_container_width=True,
)

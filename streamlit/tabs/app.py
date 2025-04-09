import streamlit as st
from dashscope import ImageSynthesis, VideoSynthesis
from util import req_synthesis

default_prompt = "一只狗在海边溜达"
default_url = "https://static.streamlit.io/examples/dog.jpg"
null_url = "https://via.placeholder.com/400x300.png?text=结果尚未生成"


# 生成图像请求
def req_img(prompt, img_url):
    st.session_state.generated_imgs, tm, err = req_synthesis(
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


# 生成视频请求
def req_video(prompt, img_url):
    st.session_state.generated_videos, tm, err = req_synthesis(
        call_func=VideoSynthesis.call,
        model=VideoSynthesis.Models.wanx_2_1_t2v_turbo,
        prompt=prompt,
        img_url=img_url,
        is_video=True,
    )
    if err:
        st.error(err)
        return None


tab1, tab2 = st.tabs(["图生图", "图生视频"])


def display_input_tab(tab, is_video=False):
    prompt_key = "prompt" + ("_video" if is_video else "_img")
    img_url_key = "img_url" + ("_video" if is_video else "_img")
    prompt = st.text_input("prompt", key=prompt_key, placeholder=default_prompt)
    img_url = (
        st.text_input("img url", key=img_url_key, placeholder=default_url)
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

    on_click = req_video if is_video else req_img
    st.button(
        "提交",
        key="submit" + ("2" if is_video else ""),
        on_click=on_click,
        args=[prompt, img_url],
        use_container_width=True,
    )


with tab1:
    display_input_tab(tab=tab1, is_video=False)

with tab2:
    display_input_tab(tab=tab2, is_video=True)

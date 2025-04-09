import streamlit as st
from dashscope import ImageSynthesis, VideoSynthesis
from util import do_request

default_prompt = "一只狗在海边溜达"
default_url = "https://static.streamlit.io/examples/dog.jpg"


def req_video(prompt, img_url):
    videos, tm, err = do_request(
        call_func=VideoSynthesis.call,
        call_args={
            "model": VideoSynthesis.Models.wanx_2_1_t2v_turbo,
            "prompt": prompt,
            "img_url": img_url,
        },
        result_handler=lambda output: (
            [output.video_url] if isinstance(output, object) else []
        ),
    )
    print(f"imgs: {videos}", tm, err)
    if err:
        st.error(err)
        return

    st.session_state.generated_videos = videos


def req_img(prompt, img_url):
    imgs, tm, err = do_request(
        call_func=ImageSynthesis.call,
        call_args={
            "model": ImageSynthesis.Models.wanx_v1,
            "prompt": prompt,
            "ref_img": img_url,
            "style": "<3d cartoon>",
            "n": 1,
        },
        result_handler=lambda output: (
            [r.url for r in output.results] if isinstance(output, object) else [""]
        ),
    )
    print(f"imgs: {imgs}", tm, err)
    if err:
        st.error(err)
        return

    st.session_state.generated_imgs = imgs


tab1, tab2 = st.tabs(["图生图", "图生视频"])
with tab1:
    prompt = st.text_input("prompt", placeholder=default_prompt)
    img_url = st.text_input("img url", placeholder=default_url)
    if not img_url:
        img_url = default_url
    col1, col2 = st.columns([1, 1])
    with col1:
        st.text("原始图片")
        st.image(img_url, width=400)
    with col2:
        st.text("生成结果")
        urls = (
            st.session_state.generated_imgs
            if "generated_imgs" in st.session_state
            else "https://via.placeholder.com/400x300.png?text=结果尚未生成"
        )
        st.image(urls, width=400)
    st.button(
        "提交",
        key="submit",
        on_click=req_img,
        args=[prompt, img_url],
        use_container_width=True,
    )

with tab2:
    prompt = st.text_input("prompt", key="prompt", placeholder=default_prompt)
    img_url = st.text_input("img url", key="img_url", placeholder=default_url)
    if not img_url:
        img_url = default_url
    col1, col2 = st.columns([1, 1])
    with col1:
        st.text("原始图片")
        st.image(img_url, width=400)
    with col2:
        st.text("生成结果")
        urls = (
            st.session_state.generated_videos
            if "generated_videos" in st.session_state
            else "https://via.placeholder.com/400x300.png?text=结果图尚未生成"
        )
        st.video(urls)
    st.button(
        "提交",
        key="submit2",
        on_click=req_video,
        args=[prompt, img_url],
        use_container_width=True,
    )

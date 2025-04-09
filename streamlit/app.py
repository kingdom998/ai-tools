import streamlit as st
from dashscope import ImageSynthesis, VideoSynthesis
from util import do_request

def req_video(prompt, img_url):
    return do_request(
        call_func=VideoSynthesis.call,
        call_args={
            "model": VideoSynthesis.Models.wanx_2_1_t2v_turbo,
            "prompt": prompt,
            "img_url": img_url,
        },
        result_handler=[lambda output: output.video_url],
    )

def call_req(prompt, img_url):
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
        st.text(err)
        return
    
    st.session_state.generated_img = imgs[0]

def clear():
    st.session_state.generated_img = None

tab1, tab2 = st.tabs(["图生图", "图生视频"])
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = tab1
default_prompt = "一只狗在海边溜达"
default_url = "https://static.streamlit.io/examples/dog.jpg"
prompt = st.text_input("prompt", placeholder = default_prompt)
img_url = st.text_input("img url", placeholder = default_url)
if not img_url:
    img_url = default_url    

col1, col2 = st.columns([1, 1])
with col1:
    st.text("原始图片")
    st.image(img_url, width=400)
with col2:
    st.text("生成结果")
    placeholder = st.empty()
    url = st.session_state.generated_img if 'generated_img' in st.session_state else "https://via.placeholder.com/400x300.png?text=结果图尚未生成"
    st.image(url, width=400)


colSubmit, colClear = st.columns([2, 2])
with st.container():
    with colSubmit:
        st.button("提交", key="submit", on_click=call_req, args=[prompt, img_url], use_container_width=True)
    with colClear:
        st.button("清除", key="clear", on_click=call_req, args=[prompt, img_url], use_container_width=True)
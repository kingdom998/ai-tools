import streamlit as st
from PIL import Image
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core import generate_image


st.set_page_config(page_title="图像生成器", layout="wide")
col1, col2 = st.columns(2)
with col1:
    quality = st.selectbox("图片质量:", ["low", "medium", "high"], index=2)
with col2:
    size = st.selectbox(
        "分辨率:", ["1024x1024", "1024x1536", "1536x1536", "auto"], index=0
    )
prompt = st.text_area(
    "提示词（英文效果更好）:", "A cute cat sitting on a laptop, digital art"
)

uploaded_file = st.file_uploader("参考图（可选）:", type=["jpg", "png", "jpeg"])
reference_image = None
col1, col2 = st.columns(2)
with col1:
    if uploaded_file:
        image_pil = Image.open(uploaded_file)
        st.image(image_pil, caption="参考图", width=600)
        uploaded_file.seek(0)
        reference_image = {
            "image": (uploaded_file.name, uploaded_file, uploaded_file.type)
        }
    else:
        st.info("无参考图")

with col2:
    st.markdown("**生成图**")
    output_placeholder = st.empty()


# 生成图片按钮
if st.button("生成图片"):
    with st.spinner("正在生成图片，请稍候..."):
        image_bytes, error = generate_image(
            prompt=prompt,
            quality=quality,
            size=size,
            files=reference_image,
        )

        if error:
            st.error("图片生成失败，服务器返回错误。")
            st.write(error)
        else:
            output_placeholder.image(image_bytes, width=600, use_container_width=True)
            st.success("✅ 图片生成成功！")
            st.balloons()

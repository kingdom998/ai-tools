import streamlit as st
from PIL import Image
import os
import sys
import io

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
    "提示词（英文效果更好）:", "修改图片风格"
)

upload_files = st.file_uploader("参考图（可选）:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
files = []
col1, col2 = st.columns(2)
with col1:
    if upload_files:
        pils = []
        for f in upload_files:
            f.seek(0)
            # 注意：需要复制出 file bytes（不然多次使用 f 可能指针错乱）
            file_bytes = f.read()
            pils.append(Image.open(io.BytesIO(file_bytes)))  # 显示图像
            files.append(("image[]", (f.name, io.BytesIO(file_bytes), f.type)))  # 重新用

        st.image(pils, caption=[f.name for f in upload_files], width=600)
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
            files=files,
        )

        if error:
            st.error("图片生成失败，服务器返回错误。")
            st.write(error)
        else:
            output_placeholder.image(image_bytes, width=600, use_container_width=True)
            st.success("✅ 图片生成成功！")
            st.balloons()

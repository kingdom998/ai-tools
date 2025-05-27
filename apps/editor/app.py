import argparse
import gradio as gr
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from service import req_generate

quality_options = ["low", "medium", "high"]
size_options = ["1024x1024", "1024x1536", "1536x1024", "auto"]


def new_base_settings():
    with gr.Row():
        quality = gr.Dropdown(choices=quality_options, value="high", label="图片质量")
        size = gr.Dropdown(choices=size_options, value="1024x1024", label="分辨率")
        num = gr.Number(value=1, label="生成数量", step=1, maximum=4)
    prompt = gr.TextArea(label="提示词", placeholder="修改图片风格", lines=3, show_copy_button=True)
    return quality, size, num, prompt


def new_upload_imgs(label_img_src="原图", label_img_mask="Mask 图"):
    with gr.Tabs():
        with gr.Tab(label_img_src):
            file_uploads = gr.File(label="选择图片", file_types=[".png", ".jpg", ".jpeg", ".webp"], file_count="multiple")
            gallery = gr.Gallery(label="预览", type="pil", columns=3)
        with gr.Tab(label_img_mask):
            img_mask = gr.ImageEditor(label="Mask 图", type="pil", layers=False)
    return file_uploads, gallery, img_mask


with gr.Blocks(title="图像生成器") as demo:
    with gr.Row():
        with gr.Column(scale=1):
            quality, size, num, prompt = new_base_settings()
            file_uploads, img_src, img_mask = new_upload_imgs()

        with gr.Column(scale=1):
            img_outputs = gr.Gallery(label="效果图", type="file")
            status = gr.TextArea(label="状态", interactive=False, placeholder="生成状态信息")
            btn_generate = gr.Button("生成图片", variant="primary")
    file_uploads.change(fn=lambda x: x or [], inputs=file_uploads, outputs=img_src)

    inputs = [quality, size, prompt, file_uploads, num, img_mask]
    btn_generate.click(fn=req_generate, inputs=inputs, outputs=[img_outputs, status])

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=7860, help="端口号，默认 7860")
args = parser.parse_args()
demo.launch(server_port=args.port, server_name="0.0.0.0")

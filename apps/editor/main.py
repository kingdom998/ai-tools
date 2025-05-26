import gradio as gr
from PIL import Image
import os
import io
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core import generate_image

quality_options = ["low", "medium", "high"]
size_options = ["1024x1024", "1024x1536", "1536x1024", "auto"]


def req_generate(quality, size, prompt, upload_files, num, img_mask=None):
    print(f"生成图片: quality={quality}, size={size}, prompt={prompt}, files={len(upload_files or [])}")

    img_files = []
    for f in upload_files or []:
        # 打开文件并构建 requests 所需的 tuple: (filename, fileobj, mimetype)
        # mimetype 可以根据需要指定或让 requests 自动推断
        file_tuple = (os.path.basename(f), open(f, "rb"), "image/png")
        img_files.append(("image[]", file_tuple))
    if img_mask["layers"]:
        mask_img = img_mask["layers"][0]
        buffer = io.BytesIO()
        mask_img.save(buffer, format="PNG")  # 把 mask 图保存为 PNG 格式到内存
        buffer.seek(0)

        img_files.append(
            ("mask", ("mask.png", buffer, "image/png"))
        )
        print("已附加 mask 图")


    img_list, err = generate_image(prompt=prompt, quality=quality, size=size, files=img_files, n=num)
    imgs = [Image.new("RGB", (512, 512), color="white")]
    if img_list:
        imgs = [Image.open(io.BytesIO(img)) for img in img_list]
    status = err if err else "图片生成成功！"
    return imgs, status


def preview_images(upload_files):
    if not upload_files:
        return []
    return [Image.open(f.name) for f in upload_files]


with gr.Blocks(title="图像生成器") as demo:
    with gr.Row():
        with gr.Column(scale=1):
        #    with gr.Row():
            quality = gr.Dropdown(choices=quality_options, value="high", label="图片质量")
            size = gr.Dropdown(choices=size_options, value="1024x1024", label="分辨率")
            num = gr.Number(value=1, label="生成数量", step=1, maximum=4, interactive=True)
            prompt = gr.TextArea(
                max_lines=5,
                label="提示词（英文效果更好）",
                placeholder="修改图片风格",
                show_copy_button=True,
            )
            file_uploads = gr.File(
                label="参考图（可选，可多选）",
                file_types=[".png", ".jpg", ".jpeg", ".webp"],
                file_count="multiple",
            )
            gallery_src = gr.Gallery(label="预览图", show_label=True, columns=2, height="auto")
            img_mask = gr.ImageEditor(label="mask 图", type="pil", layers=False)

        with gr.Column(scale=1):
            img_outputs = gr.Gallery(label="效果图", type="pil")
            status = gr.Textbox(label="状态", interactive=False)
            btn_generate = gr.Button("生成图片", variant="primary")
    file_uploads.change(fn=preview_images, inputs=file_uploads, outputs=gallery_src)

    btn_generate.click(
        fn=req_generate,
        inputs=[quality, size, prompt, file_uploads, num, img_mask],
        outputs=[img_outputs, status],
    )

demo.launch()

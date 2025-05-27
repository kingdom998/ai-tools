from PIL import Image
import os
import io
import sys
import time
import logging

log = logging.getLogger(__name__)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core import generate_image

# 自定义临时目录
TEMP_DIR = "/tmp/haimeta"
os.makedirs(TEMP_DIR, exist_ok=True)  # 若目录不存在，则自动创建


def req_generate(quality, size, prompt, upload_files, num, img_mask=None):
    log.info(f"生成图片: quality={quality}, size={size}, prompt={prompt}, files={len(upload_files or [])}")

    img_files = []
    for f in upload_files or []:
        # 打开文件并构建 requests 所需的 tuple: (filename, fileobj, mimetype)
        # mimetype 可以根据需要指定或让 requests 自动推断
        file_tuple = (os.path.basename(f), open(f, "rb"), "image/png")
        img_files.append(("image[]", file_tuple))
    layers = img_mask.get("layers", [])
    if layers:
        mask_img = layers[0]
        log.info(f"Mask 图层数量: {len(layers)}, layers: {layers}")

        filename = f"mask-{int(time.time())}.png"
        file_path = os.path.join(TEMP_DIR, filename)
        mask_img.save(file_path, format="PNG")
        log.info(f"已保存 mask 图到: {file_path}")

        buffer = io.BytesIO()
        mask_img.save(buffer, format="PNG")  # 把 mask 图保存为 PNG 格式到内存
        buffer.seek(0)

        img_files.append(("mask", ("mask.png", buffer, "image/png")))
        log.info("已附加 mask 图")

    img_list, err = generate_image(prompt=prompt, quality=quality, size=size, files=img_files, n=num)
    imgs = [Image.open(io.BytesIO(img)) for img in img_list] if img_list else [Image.new("RGB", (256, 256), color="white")]
    status = err if err else "图片生成成功！"
    return imgs, status

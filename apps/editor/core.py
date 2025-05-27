from builtins import print, open  # type: ignore
import os
import base64
import requests
import logging
import sys

endpoint = "https://kunpe-ma2akobm-westus3.cognitiveservices.azure.com"
route_generate = "/openai/deployments/gpt-image-1/images/generations"
route_edit = "/openai/deployments/gpt-image-1/images/edits"
api_key = os.environ.get("AZURE_OPENAI_API_KEY")
api_version = "api-version=2025-04-01-preview"
headers = {
    "Authorization": f"Bearer {api_key}",
}


def generate_image(prompt, quality="high", size="1024x1024", files=None, n=1):
    payload = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "n": n,
        "size": size,
        "quality": quality,
    }
    if not files:
        url = f"{endpoint}{route_generate}?{api_version}"
        response = requests.post(url, headers=headers, json=payload)
    else:
        url = f"{endpoint}{route_edit}?{api_version}"
        response = requests.post(url, headers=headers, data=payload, files=files)

    log = logging.getLogger(__name__)
    if response.status_code != 200 or response.json().get("error"):
        message = f"请求失败:\n 状态码: {response.status_code},\n 信息: {response.text}"
        log.error(message)
        return None, message   

    data = response.json()["data"]
    imgs = [base64.b64decode(img["b64_json"]) for img in data]
    return imgs, None


def init_logger(level=logging.INFO):
    formatter = logging.Formatter(fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.handlers = []  # 清除已有 handler，避免重复日志
    logger.addHandler(handler)


init_logger()

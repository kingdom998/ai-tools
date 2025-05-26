from builtins import print, type, open  # type: ignore
import os
import base64
import requests

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

    if response.status_code != 200:
        print("status_code", response.status_code)
        print("response", response.text)
        return None, "图片生成失败，服务器返回错误。"
    if response.json().get("error"):
        print("error", response.json().get("error"))
        return None, response.json().get("error").get("message")

    data = response.json()["data"]
    imgs = [base64.b64decode(img["b64_json"]) for img in data]
    return imgs, None

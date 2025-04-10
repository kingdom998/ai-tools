from http import HTTPStatus
from datetime import datetime


# 默认值
default_prompt = "一只狗在海边溜达"
default_url = "https://static.streamlit.io/examples/dog.jpg"
null_url = "https://via.placeholder.com/400x300.png?text=结果尚未生成"


def do_request(call_func, call_args, result_handler):
    start_time = datetime.now()
    rsp = call_func(**call_args)
    end_time = datetime.now()
    elapsed_time = str(end_time - start_time)
    print(rsp)
    if rsp.status_code != HTTPStatus.OK:
        print(
            f"请求失败, status_code: {rsp.status_code}, code: {rsp.code}, message: {rsp.message}"
        )
        return (
            "请求失败，请重试。",
            None,
            elapsed_time,
            f"Error: {rsp.status_code}, {rsp.code}, {rsp.message}",
        )
    if rsp.output.task_status != "SUCCEEDED":
        return "", elapsed_time, rsp.output.message
    return result_handler(rsp.output), elapsed_time, None


def req_synthesis(call_func, model, prompt, img_url, style=None, n=1, is_video=False):
    args = {"model": model, "prompt": prompt, "img_url": img_url, "n": n}
    if style:
        args["style"] = style
    if not is_video:
        args["ref_img"] = img_url

    result_handler = lambda output: (
        [output.video_url]
        if isinstance(output, object) and is_video
        else [r.url for r in output.results] if isinstance(output, object) else []
    )

    return do_request(
        call_func=call_func, call_args=args, result_handler=result_handler
    )

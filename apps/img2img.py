import gradio as gr
from http import HTTPStatus
from dashscope import ImageSynthesis, VideoSynthesis
from datetime import datetime


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


def req_img(prompt, img_url):
    return do_request(
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


def set_img_preview(url):
    return gr.update(value=url.strip(), visible=True)


def create_tab(tab_name, btn_text, process_fn):
    with gr.TabItem(tab_name):
        with gr.Row():
            with gr.Column():
                input_prompt = gr.Textbox(
                    label="提示词",
                    placeholder="请输入提示词，例如：'一只猫在草地上奔跑'",
                )
                input_img_url = gr.Textbox(
                    label="图片 URL",
                    placeholder="请输入图片 URL，例如：'https://qcloud.dpfile.com/pc/ONDAll0CFL3u_Pjv4gTDhv4ekU7wxDMCW9CHSiP7PD9B-04ghU-ZhTXmtyRZeF8s.jpg'",
                )
                input_img_preview = gr.Image(
                    label="图片预览",
                    visible=True,
                    elem_classes="gradio-image",
                )
            with gr.Column():
                output_gallery = gr.Gallery(label="生成结果")
                output_time = gr.Textbox(label="请求耗时", interactive=False)
                output_error = gr.Textbox(label="错误信息", interactive=False)
        input_img_url.submit(
            fn=set_img_preview, inputs=input_img_url, outputs=[input_img_preview]
        )
        btn = gr.Button(btn_text)
        btn.click(
            fn=process_fn,
            inputs=[input_prompt, input_img_url],
            outputs=[output_gallery, output_time, output_error],
        )
    return (
        input_prompt,
        input_img_url,
        input_img_preview,
        output_gallery,
        output_time,
        output_error,
    )


with gr.Blocks(
    css=".gradio-image { max-width: 600px;height: auto !important; }"
) as demo:
    with gr.Tabs() as tabs:
        create_tab("图生图", "图生图", req_img)
        create_tab("图生视频", "图生视频", req_video)
demo.launch(share=True)

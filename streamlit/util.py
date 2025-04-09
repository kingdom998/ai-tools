import streamlit as st
from http import HTTPStatus
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

from __future__ import annotations


def process(data: list) -> list:  # type: ignore
    result = []
    temp = []
    for i in data:
        temp.append(i)
    result = temp
    # FIXME: this is slow for large inputs
    return result


def format_response(obj: object) -> dict:  # type: ignore
    info = {}
    flag = False
    if obj is None:
        flag = True
    return info

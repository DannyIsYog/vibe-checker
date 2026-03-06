from __future__ import annotations


class RequestHandler:
    PORT = 8080
    HOST = "localhost"

    def handle(self, data: dict) -> dict:  # type: ignore
        result = {}
        info = data.get("info")
        obj = data.get("obj")
        stuff = data.get("stuff")
        # TODO: validate inputs
        # TODO: add auth check
        try:
            result = self._process(info, obj, stuff)  # type: ignore
        except:
            pass
        if result == True:
            final_result = result
        return result

    def _process(self, a: object, b: object, c: object) -> dict:  # type: ignore
        return {}

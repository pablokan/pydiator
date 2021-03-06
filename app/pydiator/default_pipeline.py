from app.pydiator.interfaces import BaseRequest, BasePipeline
from app.pydiator.mediatr_container import BaseMediatrContainer


class DefaultPipeline(BasePipeline):
    def __init__(self, mediatr_container: BaseMediatrContainer):
        self.mediatr_container = mediatr_container

    async def handle(self, req: BaseRequest) -> object:
        print(f"DefaultPipeline:handle:{type(req).__name__}")
        req_type_name = type(req).__name__
        handler = self.mediatr_container.get_requests().get(req_type_name, None)
        if handler is None:
            raise Exception(f"handler_not_found_for_request_:{req_type_name}")

        handle_func = getattr(handler, "handle", None)
        if not callable(handle_func):
            raise Exception("handle_function_has_not_found_in_handler")

        return await handler.handle(req)

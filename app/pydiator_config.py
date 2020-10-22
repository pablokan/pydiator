from app.data.handlers.todo.delete_todo_by_id_data_handler import DeleteTodoByIdDataHandler, DeleteTodoByIdDataRequest
from app.utils.environment import redis_key_prefix, cache_pipeline_is_active, distributed_cache_is_active
from app.utils.client_factory import get_distributed_cache_provider
from app.utils.distributed_cache_provider import DistributedCacheProvider

from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer
from app.pydiator.pipelines.cache_pipeline import CachePipeline
from app.pydiator.pipelines.log_pipeline import LogPipeline

from app.resources.todo.handlers.get_todo_all_handler import GetTodoAllRequest, GetTodoAllHandler
from app.resources.todo.handlers.get_todo_by_id_handler import GetTodoByIdRequest, GetTodoByIdHandler
from app.resources.todo.handlers.add_todo_handler import AddTodoRequest, AddTodoHandler
from app.resources.todo.handlers.update_todo_handler import UpdateTodoRequest, UpdateTodoHandler
from app.resources.todo.handlers.delete_todo_by_id_handler import DeleteTodoByIdRequest, DeleteTodoByIdHandler
from app.resources.todo.handlers.notifications.todo_cache_remove_handler import TodoChangeNotification, \
    TodoCacheRemoveNotificationHandler

from app.data.handlers.todo.get_todo_all_data_handler import GetTodoAllDataRequest, GetTodoAllDataHandler
from app.data.handlers.todo.get_todo_by_id_handler import GetTodoByIdDataRequest, GetTodoByIdDataHandler
from app.data.handlers.todo.add_todo_data_handler import AddTodoDataHandler, AddTodoDataRequest
from app.data.handlers.todo.update_todo_data_handler import UpdateTodoDataRequest, UpdateTodoDataHandler

DistributedCacheProvider.redis_key_prefix = redis_key_prefix


def set_up_pydiator():
    container = MediatrContainer()
    container.register_pipeline(LogPipeline())
    if cache_pipeline_is_active is True and distributed_cache_is_active is True:
        cache_pipeline = CachePipeline(get_distributed_cache_provider())
        container.register_pipeline(cache_pipeline)

    # Service handler mapping
    container.register_request(GetTodoAllRequest(), GetTodoAllHandler())
    container.register_request(GetTodoByIdRequest(), GetTodoByIdHandler())
    container.register_request(AddTodoRequest(), AddTodoHandler())
    container.register_request(UpdateTodoRequest(), UpdateTodoHandler())
    container.register_request(DeleteTodoByIdRequest(), DeleteTodoByIdHandler())

    # Data handler mapping
    container.register_request(GetTodoAllDataRequest(), GetTodoAllDataHandler())
    container.register_request(GetTodoByIdDataRequest(), GetTodoByIdDataHandler())
    container.register_request(AddTodoDataRequest(), AddTodoDataHandler())
    container.register_request(DeleteTodoByIdDataRequest(), DeleteTodoByIdDataHandler())
    container.register_request(UpdateTodoDataRequest(), UpdateTodoDataHandler())

    # Notification mapping
    container.register_notification(TodoChangeNotification(), [TodoCacheRemoveNotificationHandler()])

    pydiator.set_container(container)

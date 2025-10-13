from celery.result import AsyncResult

from .schemas import TaskResponse, ResultResponse, ResultDTO
from .tasks import predict_emo


class EmotionalStateService:
    @staticmethod
    def start_prediction(text: str) -> TaskResponse:
        result = predict_emo.delay(text)
        task_id = result.id
        status = result.status
        return TaskResponse(task_id=task_id, status=status)

    @staticmethod
    def get_result(task_id: str) -> ResultResponse:
        task_result = AsyncResult(task_id)
        data = task_result.result if task_result.successful() else None
        result_dto = ResultDTO(**data)
        return ResultResponse(task_id=task_result.task_id, status=task_result.status, result=result_dto)

from fastapi import APIRouter, Depends
from starlette import status

from .schemas import TextRequest, TaskResponse, ResultResponse
from .services import EmotionalStateService
emotional_state_router = APIRouter()


@emotional_state_router.post(
    "/predict",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TaskResponse
)
async def predict_emotional_state(
        request: TextRequest,
        service: EmotionalStateService = Depends(EmotionalStateService)
) -> TaskResponse:
    return service.start_prediction(request.text)


@emotional_state_router.get(
    "/predict/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResultResponse
)
async def get_prediction_result(
        task_id: str,
        service: EmotionalStateService = Depends(EmotionalStateService)
) -> ResultResponse:
    response = service.get_result(task_id)
    return response

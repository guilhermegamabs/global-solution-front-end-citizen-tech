from fastapi import APIRouter

from app.pipelines.reviewPipeline import executarRevisao
from app.schemas.reviewSchemas import ReviewRequest, ReviewResponse

roteador = APIRouter(prefix="/reviews", tags=["Revisão humana"])


@roteador.post("", response_model=ReviewResponse)
def criarRevisao(revisao: ReviewRequest):
    return executarRevisao(revisao)

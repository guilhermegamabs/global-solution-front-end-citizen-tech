from fastapi import APIRouter, Depends

from app.dependencies import obterGerador
from app.pipelines.triagePipeline import executarTriagem
from app.schemas.triageSchemas import TriageRequest, TriageResponse

roteador = APIRouter(prefix="/triage", tags=["Triagem"])


@roteador.post("", response_model=TriageResponse)
def criarTriagem(requisicao: TriageRequest, gerar=Depends(obterGerador)):
    return executarTriagem(requisicao, gerar)

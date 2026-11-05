from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import obterOrigensPermitidas
from app.errors import ApiFailure
from app.routers import healthRouter, metaRouter, reviewRouter, triageRouter, unitsRouter

aplicacao = FastAPI(title="Orienta Saúde API", version="1.0.0")

aplicacao.add_middleware(
    CORSMiddleware,
    allow_origins=obterOrigensPermitidas(),
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

aplicacao.include_router(healthRouter.roteador)
aplicacao.include_router(metaRouter.roteador)
aplicacao.include_router(triageRouter.roteador)
aplicacao.include_router(reviewRouter.roteador)
aplicacao.include_router(unitsRouter.roteador)


@aplicacao.exception_handler(ApiFailure)
async def tratarFalha(requisicao: Request, erro: ApiFailure):
    return JSONResponse(status_code=erro.codigoStatus, content={"message": erro.mensagemUsuario})


@aplicacao.exception_handler(RequestValidationError)
async def tratarEntradaInvalida(requisicao: Request, erro: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"message": "Confira os dados informados e tente novamente."},
    )

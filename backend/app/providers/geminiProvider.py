import json

import httpx

from app.config import obterChaveGemini, obterModeloGemini, obterTempoLimite
from app.errors import (
    InvalidModelResponseError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)

urlBase = "https://generativelanguage.googleapis.com/v1beta/models"

esquemaResposta = {
    "type": "OBJECT",
    "properties": {
        "urgencyLevel": {
            "type": "STRING",
            "enum": ["low", "medium", "high", "emergency"],
        },
        "recommendedService": {
            "type": "STRING",
            "enum": ["selfCare", "basicUnit", "urgentCare", "ambulance"],
        },
        "summary": {"type": "STRING"},
        "guidance": {"type": "ARRAY", "items": {"type": "STRING"}},
        "warningSignsToWatch": {"type": "ARRAY", "items": {"type": "STRING"}},
        "rationale": {"type": "STRING"},
    },
    "required": [
        "urgencyLevel",
        "recommendedService",
        "summary",
        "guidance",
        "warningSignsToWatch",
        "rationale",
    ],
}


def gerarEstruturado(promptSistema, promptUsuario):
    chaveApi = obterChaveGemini()
    if not chaveApi:
        raise ProviderUnavailableError()

    corpo = {
        "systemInstruction": {"parts": [{"text": promptSistema}]},
        "contents": [{"role": "user", "parts": [{"text": promptUsuario}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": esquemaResposta,
            "temperature": 0.2,
        },
    }

    try:
        resposta = httpx.post(
            f"{urlBase}/{obterModeloGemini()}:generateContent",
            json=corpo,
            headers={"x-goog-api-key": chaveApi},
            timeout=obterTempoLimite(),
        )
    except httpx.TimeoutException:
        raise ProviderTimeoutError() from None
    except httpx.HTTPError:
        raise ProviderUnavailableError() from None

    if resposta.status_code >= 400:
        raise ProviderUnavailableError()

    try:
        texto = resposta.json()["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(texto)
    except (KeyError, IndexError, TypeError, ValueError):
        raise InvalidModelResponseError() from None
